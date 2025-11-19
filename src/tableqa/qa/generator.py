"""
Q/A pair generation from statistical insights.

Converts facts into multiple question/answer pairs using:
1. Template-based generation
2. LLM paraphrasing and augmentation
"""

import json
import logging
from typing import Any

try:
    import openai

    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

from tableqa.qa.templates import QuestionTemplate, infer_question_type

logger = logging.getLogger(__name__)


class QAGenerator:
    """Generates Q/A pairs from statistical insights."""

    def __init__(
        self,
        use_llm: bool = False,
        llm_provider: str = "openai",
        llm_model: str | None = None,
        api_key: str | None = None,
        paraphrase_count: int = 2,
    ) -> None:
        """
        Initialize Q/A generator.

        Args:
            use_llm: Whether to use LLM for paraphrasing
            llm_provider: LLM provider ('openai' or 'anthropic')
            llm_model: Model name
            api_key: API key for LLM
            paraphrase_count: Number of paraphrased versions per question
        """
        self.use_llm = use_llm
        self.paraphrase_count = paraphrase_count

        if use_llm:
            if llm_provider == "openai":
                if not HAS_OPENAI:
                    raise ImportError("openai required for LLM features")
                self.client = openai.OpenAI(api_key=api_key) if api_key else openai.OpenAI()
                self.model = llm_model or "gpt-4"
            else:
                raise ValueError(f"LLM provider {llm_provider} not yet supported for Q/A generation")

    def generate_qa_pairs(
        self, insight: dict[str, Any], formatted_answer: str
    ) -> list[dict[str, str]]:
        """
        Generate Q/A pairs from a statistical insight.

        Args:
            insight: Statistical analysis result
            formatted_answer: Natural language answer

        Returns:
            List of Q/A pair dictionaries with keys: question, answer, type
        """
        # Infer question type
        q_type = infer_question_type(insight)

        # Generate template-based questions
        template = QuestionTemplate(q_type)
        qa_pairs = template.generate(insight, formatted_answer)

        # LLM paraphrasing
        if self.use_llm and qa_pairs:
            try:
                paraphrased = self._paraphrase_questions(qa_pairs, insight)
                qa_pairs.extend(paraphrased)
            except Exception as e:
                logger.warning(f"LLM paraphrasing failed: {e}")

        return qa_pairs

    def generate_batch(
        self, insights: list[dict[str, Any]], formatted_answers: list[str]
    ) -> list[dict[str, Any]]:
        """
        Generate Q/A pairs for multiple insights.

        Args:
            insights: List of statistical insights
            formatted_answers: Corresponding natural language answers

        Returns:
            List of insight dictionaries with added 'qa_pairs' field
        """
        results = []

        for insight, answer in zip(insights, formatted_answers):
            qa_pairs = self.generate_qa_pairs(insight, answer)

            result = insight.copy()
            result["formatted_answer"] = answer
            result["qa_pairs"] = qa_pairs
            results.append(result)

        return results

    def _paraphrase_questions(
        self, qa_pairs: list[dict[str, str]], insight: dict[str, Any]
    ) -> list[dict[str, str]]:
        """
        Use LLM to generate paraphrased questions.

        Args:
            qa_pairs: Original Q/A pairs
            insight: Statistical insight for context

        Returns:
            List of paraphrased Q/A pairs
        """
        # Take first few original questions
        original_questions = [qa["question"] for qa in qa_pairs[:3]]
        answer = qa_pairs[0]["answer"] if qa_pairs else ""

        prompt = f"""Given these questions about a statistical finding, generate {self.paraphrase_count} natural paraphrases for each.

Original Questions:
{chr(10).join(f'{i+1}. {q}' for i, q in enumerate(original_questions))}

Answer (for context):
{answer}

Generate paraphrased questions that:
1. Ask for the same information in different ways
2. Vary in formality and structure
3. Could include domain-specific terminology
4. Remain clear and answerable

Return as JSON array with format:
[
  {{"original": "question 1", "paraphrases": ["p1", "p2"]}},
  ...
]
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are helping create a diverse Q/A dataset for data analysis.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=800,
                temperature=0.7,  # Higher temperature for diversity
            )

            content = response.choices[0].message.content or ""

            # Extract JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            paraphrase_data = json.loads(content.strip())

            # Build Q/A pairs from paraphrases
            paraphrased_pairs = []
            for item in paraphrase_data:
                for paraphrase in item.get("paraphrases", []):
                    paraphrased_pairs.append({
                        "question": paraphrase,
                        "answer": answer,
                        "type": qa_pairs[0]["type"] if qa_pairs else "descriptive",
                        "source": "llm_paraphrase",
                    })

            return paraphrased_pairs

        except Exception as e:
            logger.warning(f"Failed to paraphrase questions: {e}")
            return []

    def generate_exploratory_questions(
        self, insight: dict[str, Any], context: str | None = None
    ) -> list[str]:
        """
        Generate exploratory follow-up questions using LLM.

        Args:
            insight: Statistical insight
            context: Optional dataset/domain context

        Returns:
            List of exploratory questions
        """
        if not self.use_llm:
            return []

        context_str = f"\n\nContext: {context}" if context else ""

        prompt = f"""Based on this statistical finding, generate 5 insightful follow-up questions that would deepen understanding.

Finding:
{json.dumps(insight, indent=2)}{context_str}

Generate questions that:
1. Explore mechanisms or explanations
2. Identify potential confounders or moderators
3. Suggest practical implications
4. Consider alternative explanations
5. Propose related analyses

Return as a JSON array of strings: ["question 1", "question 2", ...]
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a research methodologist helping design data analysis studies.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=600,
                temperature=0.8,
            )

            content = response.choices[0].message.content or ""

            # Extract JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            questions = json.loads(content.strip())
            return questions if isinstance(questions, list) else []

        except Exception as e:
            logger.warning(f"Failed to generate exploratory questions: {e}")
            return []

    def export_qa_dataset(
        self, qa_results: list[dict[str, Any]], output_format: str = "jsonl"
    ) -> list[str]:
        """
        Export Q/A pairs in format suitable for LLM fine-tuning.

        Args:
            qa_results: Results from generate_batch
            output_format: 'jsonl', 'openai', or 'anthropic'

        Returns:
            List of formatted strings (one per line for JSONL)
        """
        lines = []

        for result in qa_results:
            for qa in result.get("qa_pairs", []):
                if output_format == "jsonl":
                    lines.append(json.dumps(qa, ensure_ascii=False))

                elif output_format == "openai":
                    # OpenAI fine-tuning format
                    entry = {
                        "messages": [
                            {"role": "system", "content": "You are a data analyst answering questions about statistical findings."},
                            {"role": "user", "content": qa["question"]},
                            {"role": "assistant", "content": qa["answer"]},
                        ]
                    }
                    lines.append(json.dumps(entry, ensure_ascii=False))

                elif output_format == "anthropic":
                    # Anthropic format (simpler)
                    entry = {
                        "prompt": qa["question"],
                        "completion": qa["answer"],
                    }
                    lines.append(json.dumps(entry, ensure_ascii=False))

        return lines
