from ai_rewriter import rewrite_article

# Replace this with an actual article ID from the database
original_article_id = 1  # Change this if needed

# The article text that needs to be rewritten
test_text = "Helsingin Sanomat kertoo, että Suomessa on liian vähän maahanmuuttajia."

# Now passing BOTH required arguments
rewritten_text = rewrite_article(original_article_id, test_text)

print("Uudelleenkirjoitettu artikkeli:\n", rewritten_text)