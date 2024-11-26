# import language_tool_python
#
# # Initialize the tool for English language
# tool = language_tool_python.LanguageTool('en-US')
#
#
# # Function to score a sentence out of 5
# def score_sentence(text):
#     # Maximum score is 5
#     max_score = 5
#
#     # Check for grammar mistakes
#     matches = tool.check(text)
#
#     # If there are no matches (i.e., no mistakes), return full score
#     if not matches:
#         return max_score
#
#     # Calculate the number of mistakes
#     total_mistakes = len(matches)
#
#     # We can deduct points based on the number of mistakes
#     # For simplicity, we assume:
#     # - 0 mistakes = 5 points (perfect sentence)
#     # - 1-2 mistakes = 4 points (good sentence)
#     # - 3-4 mistakes = 3 points (average)
#     # - 5-6 mistakes = 2 points (below average)
#     # - 7+ mistakes = 1 point (poor sentence)
#
#     if total_mistakes == 0:
#         return 5
#     elif total_mistakes <= 2:
#         return 4
#     elif total_mistakes <= 4:
#         return 3
#     elif total_mistakes <= 6:
#         return 2
#     else:
#         return 1

#
# # Example usage
# text1 = "This is an exampel of a sentence with bad grammer."
# text2 = "This is an example of a sentence with perfect grammar."
#
# score1 = score_sentence(text1)
# score2 = score_sentence(text2)
#
# print(f"Sentence: '{text1}'\nScore: {score1}/5")
# print(f"Sentence: '{text2}'\nScore: {score2}/5")


from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage



def sentence_score(model, text):
    message = [
        SystemMessage(
            content="You are a language model that specializes in evaluating the grammatical and spelling quality of sentences. "
                    "Please rate the sentence below out of 5, where 5 is perfect and 0 is the worst. The outcome should only be a number between 0 and 5, and nothing else."
        ),
        HumanMessage(content=f"Please evaluate this sentence: {text}")
    ]

    result = model.invoke(message)
    parser = StrOutputParser()
    return int(parser.invoke(result))