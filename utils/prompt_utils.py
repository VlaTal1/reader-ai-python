FORMAT = '''{
    question: str,
    quote: str,
    answers: [
        {
            answer: str,
            correct: boolean,
        }
    ]
}'''

TOPICS = '''1. questions about the personalities of the characters
2. questions about the appearance or look of characters
3. what the characters did in certain situations
4. what the characters did in certain situations, what they thought or felt
5. the attitude of some characters to other characters
6. names of cities or locations where the events took place
7. what are the key characters'''

PROMPT = '''You are an experienced educational content creator specializing in reading comprehension exercises for children. Your task is to create a single, clear, and specific multiple-choice question based on a given book excerpt.

First, carefully read the following book excerpt:

<book_excerpt>
{}
</book_excerpt>

Now, review this list of topics that may be relevant to the question you'll create:

<topics_list>
{}
</topics_list>

Your goal is to create ONE question for children who have read this excerpt. Follow these guidelines:

1. The question must be closely related to the content of the text.
2. Generate 4 answer choices, with only 1 correct answer.
3. Use language and style similar to the text itself.
4. Avoid creating tricky or intentionally misleading questions or answers.
5. The question must be in the same language as the book excerpt.
6. Ensure the question is clear and specific, explicitly mentioning any relevant context from the excerpt.

Before creating your final question, wrap your reasoning process in <question_development> tags. Follow these steps:

1. Identify 2-3 key quotes from the excerpt that could be potential question sources. Write these quotes down verbatim.
2. List 3-4 relevant topics from the provided topic list that relate to these quotes.
3. For each potential question:
   - Formulate a clear and concise question, ensuring it includes specific context.
   - Write the correct answer and three plausible but incorrect answers.
   - Evaluate the question based on clarity, relevance, and difficulty level.
   - Consider the age-appropriateness of the question for children.
   - Assess how well the question aligns with the provided topics.
4. Choose the best question based on your evaluation.
5. Select the relevant quote that corresponds to your chosen question.
6. Explain why the chosen question is the best option, considering all factors evaluated.

After your question development process, provide the final output as a JSON object in <json_format> wrapper. Here's the required format:

<json_format>
{}
</json_format>

Remember, the "quote" field should contain the specific part of the text from which you derived the question.'''


def get_prompt(text_part: str):
    return PROMPT.format(text_part, TOPICS, FORMAT)
