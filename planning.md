# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- The domain that I chose is student experiences with on-campus dining halls and off-campus food spots around the University of Florida, Gainesville. This knowledge is valuable for incoming students who have never been to Gainesville and want a better idea of what's available on and off campus and whether it is worth it to purchase the expensive meal plan. Knowledge about on and off campus food spots are hard to find through official channels as they promote dining halls and restaraunts that would benefit the university rather than providing an unbiased opinion.  -->
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit Thread  | Student opinions on meal plan prices | https://www.reddit.com/r/ufl/comments/1szl19w/new_uf_meal_plans_breakdown/ |
| 2 | UF Florida Fresh Dining Website | Official meal plans and locations of on-campus food spots listed | https://dineoncampus.com/UF |
| 3 | SwampRentals | Blog written by a UF student about off-campus restaraunts | https://www.swamprentals.com/help-finding-apartments/what-restaurants-are-near-uf-campus |
| 4 | The Alligator | Student written article on an on-campus dining hall reopening | https://www.alligator.org/article/2024/08/the-eatery-at-broward-hall-first-look |
| 5 | The Alligator | Student written article on off-campus dining spots | https://www.alligator.org/article/2025/08/a-new-student-s-guide-to-the-gainesville-food-scene |
| 6 | Conference Guide | Food guide for places to eat and stay in Gainesville, close to the campus | https://writing.ufl.edu/wp-content/uploads/sites/101/2020/01/Guide-for-the-2020-Pedagogy.pdf |
| 7 | Prked | Guide on breaking down UF's meal plans along with Pros and Cons | https://prked.com/post/guide-to-uf-meal-plans-2024-2025 |
| 8 | Spoon University | Guide to the best vegan restaraunts in Gainesville | https://spoonuniversity.com/school/ufl/best-vegan-options-in-gainesville-florida/ |
| 9 | UF Department of Neurology | Popular Restaraunts in Gainesville | https://neurology.ufl.edu/living-in-gainesville/popular-restaurants/ |
| 10 | The Alligator  | Alternative to student meal plans | https://www.alligator.org/article/2024/09/what-to-know-about-a-new-student-meal-plan-alternative |
---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size: 150 - 300 words**

**Overlap: around 30 words**

**Reasoning: A chunk size of 150-300 words fits this set of documents as they are very review-heavy and present recommendations on places to dine, rather than include long explanations. The sources listed above have natural units, such as paragraphs or list entries, that contain a set of information like the restaraunt name, the author's opinion, along with location and price. The overlap size of around 30 words fits the structure of my documents as there could be overlap between the various article sources where prior context or locations are mentioned.**
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model: all-MiniLM-L6-v2 via sentence transformers**

**Top-k: 5**

**Production tradeoff reflection: If I was deploying this for real users and cost was not a constraint, the embedding model I would use is text-embedding-3-large via the OpenAI API. This is because it offers a larger context window of 8,191 tokens, when compared to all-MiniLM-L6-v2 which offers 256 tokens. IT also offers higher accuracy on retrieval benchmarks and better understanding of student language, since the target audience is college students who would speak informally. In choosing this embedding model, the tradeoffs are API cost and network latency on each query.**
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What are on-campus food options at UF? | Pull answer from food guides with information about restaraunts and their locations |
| 2 | According to students, is the UF meal plan worth buying? | Pull answer from Prked guide and break down prices and value of each type of meal plan |
| 3 | What vegan or vegetarian food options are available near UF campus? | Pull answer from Spoon University's food guide and the Alligator's vegan article |
| 4 | What are students' opinions about dining halls on campus? | Pull answer from Reddit about student's reviews on dining hall food |
| 5 | What are cheap but some of the best food options available near UF campus for new students? | Pull answer from the Alligator's new student guide and SwampRentals blog |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. The first anticipated challenge is that multiple of my sources could contain the same information about on and off campus dining areas. Since Gainesville is more of a college city, there are only so many food places available. Therefore, a number of food spots appear in almost every source about food areas in Gainesville. So, when the user asks about different restaraunts on or off campus, the information about the food spots might vary while the food spots themselves might stay the same.

2. Another anticipated challenge is that some sources might have outdated information. Since my sources range from 2017 to 2025, certain restaraunts might have closed or changed locations, so the user receives outdated information from their search. The challenge is that the AI is not going to know whether the information is accurate or not, it is simply going to present the information it received from the chunks. 

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

<!-- Document Ingestion (Manual .txt files) -> Chunking (LangChain RecursiveCharacterTextSpliier) -> Embedding + Vector Store (all-MiniLM-L6-v2 via sentence transformers + ChromaDB) -> Retrieval (top-k = 5, ChromaDB) -> Generation (Claude API) -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. 
     
     **Document Ingestion:** 
     Tool: Claude
     Input: List of 10 sources above and document type
     Expected Ouput: Code that loads pre-saved .txt files using open() and .read() and stores them in a list with different attributes, such as source, description, URL, etc.
     Verify Output: Print the number of characters of each loaded source to ensure that it matches the length of the original document 

     **Chunking:**
     Tool: Claude
     Input: Chunk size: 150-300 words, overlap: 30 words, create chunks by splitting paragraphs from guides and articles and splitting comments from Reddit
     Expected Output: a function with parameters: chunk_size and chunk_overlap, created using LangChain RecursiveCharacterTextSplitter
     Verify Output: Run the function from the output on one of my documents and read through the chunks to ensure they are the right size and contain the right content

     **Embedding + Vector Store:**
     Tool: Claude
     Input: My architecture diagram from the previous subsection showing all of the steps and tools necessary
     Expected Output: Code that embeds all of the necessary chunks using all-MiniLM-L6-v2 via sentence-transformers and stores them in the database
     Verify Output: Check the database count to ensure it matches the total number of chunks across all 10 sources 

     **Retrieval:**
     Tool: Claude
     Input: top-k = 5, ChromaDB, and all-MiniLM-L6-v2 via sentence-transformers
     Expected Output: function that takes in a query string, embeds it, and returns the top 5 chunks along with their source
     Verify Output: test my questions from a previous subsection to verify whether the output is relevant to the question and accurate 

     **Generation:**
     Tool: Claude
     Input: My retrieval output and description of my domain
     Expected Output: a function that takes a query and the top 5 chunks for that query to sent to Claude API with a system prompt which tells the API to answer according to the domain
     Verify Output: test my question from a previous subsection and ensure that the answers are using my various sources and not using inaccurate information or making its own assumptions.
    
     -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
