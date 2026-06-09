# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- The domain that I chose is student experiences with on-campus dining halls and off-campus food spots around the University of Florida, Gainesville. This knowledge is valuable for incoming students who have never been to Gainesville and want a better idea of what's available on and off campus and whether it is worth it to purchase the expensive meal plan. Knowledge about on and off campus food spots are hard to find through official channels as they promote dining halls and restaraunts that would benefit the university rather than providing an unbiased opinion. -->

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size: 300 characters**

**Overlap: 30 characters**

**Why these choices fit your documents: A chunk size of 150-300 words fits this set of documents as they are very review-heavy and present recommendations on places to dine, rather than include long explanations. The sources listed above have natural units, such as paragraphs or list entries, that contain a set of information like the restaraunt name, the author's opinion, along with location and price. The overlap size of around 30 words fits the structure of my documents as there could be overlap between the various article sources where prior context or locations are mentioned.**

**Preprocessing: Before chunking, each document was clearned to ensure that HTML tags were removed along with navbars, banners, and random text. The only content that was kept was information about restaraunts, such as locations, descriptions, and pricing.**

**Final chunk count: 222, a minimum length filter of 100 characters was applied as it removed header-only fragments in various sources as they did not contain of useful information or content.**
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used: all-MiniLM-L6-v2 via sentence transformers**

**Production tradeoff reflection: If I was deploying this for real users and cost was not a constraint, the embedding model I would use is text-embedding-3-large via the OpenAI API. This is because it offers a larger context window of 8,191 tokens, when compared to all-MiniLM-L6-v2 which offers 256 tokens. IT also offers higher accuracy on retrieval benchmarks and better understanding of student language, since the target audience is college students who would speak informally. In choosing this embedding model, the tradeoffs are API cost and network latency on each query.**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction: The system prompt passed to llama-3.3-70b-versatile instructs the model to answer only from the provided context passages: 

You are a helpful dining and meal plan guide for students at the University of Florida (UF).

You will be given a question and a set of context passages retrieved from UF dining and restaurant documents.

Rules you must follow:
1. Answer ONLY using the information found in the provided context passages.
2. Do NOT use any outside knowledge or make assumptions beyond what is in the context.
3. If the context does not contain enough information to answer the question, respond with exactly: "I don't have enough information on that."
4. Be concise and helpful. Write in a friendly tone suited for a college student.
5. Do not mention the context passages or that you are reading from documents — just answer naturally.**

**How source attribution is surfaced in the response: Source attribution is handled before the LLM is called as source names are pulled directory from chunk metadata and returned as a separate list. The Gradio Interface displays the sources in a separate field under the "Answer" box in a "Retrieved from" field, regardless of what the LLM says in response to the prompt.**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | How much does it cost to eat at Broward dining hall? | Pull answer from UF Florida Fresh Dining and Reddit that break meal plans and their prices | Returned exact pricing — $12.33 + tax without a swipe, $9.30 breakfast, $11.40 lunch, $12.00 dinner | Relevant | Accurate |
| 2 | According to students, is the UF meal plan worth buying? | Pull answer from Prked guide and break down prices and value of each type of meal plan | Returned mixed opinions — one student found cooking cheaper, another considered a lower plan for convenience | Partially relevant | Partially accurate |
| 3 | What vegan or vegetarian food options are available near UF campus? | Pull answer from Spoon University's food guide and the Alligator's vegan article | Returned The Top, Reggae Shack, and Karma Cream with brief descriptions | Relevant | Accurate |
| 4 | What are students' opinions about dining halls on campus? | Pull answer from Reddit about student's reviews on dining hall food | Returned mixed sentiment — one student disliked dining halls, others described them as social hubs | Partially relevant | Partially accurate |
| 5 | What are cheap but some of the best food options available near UF campus for new students? | Pull answer from the Alligator's new student guide and SwampRentals blog | Returned only Chopstix with minimal detail, missing many affordable options in the corpus | Off-target | Inaccurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed: What are cheap but good food options near UF for new students?**

**What the system returned: Only Chopstix was mentioned as a specific recommendation with minimal detail, despite the corpus containing many affordable restaurant options across multiple sources.**

**Root cause (tied to a specific pipeline stage): The cause of this has to do with the retrieval stage of the pipeline. Because the query is broad, it matches to various chunks very loosely rather than precisely. The top-k=5 results pulled chunks from several different sources rather than looking for recommendations from a single source, so it led to more a vague answer. Ultimately, the response to the question was not strong enough because no chunks contained information about affordable options at UF to give the LLM sufficient information and context for a more accurate and specific answer.**

**What you would change to fix it: To fix this issue, increasing the chunk size to around 500 characters would help related text to stay together in a single chunk. Along with that, increasing the top-k value from 5 to 8 would help address broader queries and reduce the chance that relevant chunks are missed or not considered in the answer.**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation: One way the spec helped me during implementation was having the chunking strategy section figured out before actually implementing that step. Since that section of the planning.md was already filled out, I knew exactly how to prompt the AI with specific numbers, which made it easier to implement the functions and generate the chunks. Because of this, I did not have to make a guess on what I wanted the chunk size and overlap to be.**

**One way your implementation diverged from the spec, and why: One way my implementation diverged from the spec was having to measure the chunk size in characters instead of words because LangChain's RecursiveCharacterTextSplitter measures in characters. Other than that, the spec did not mention the need for a minimum chunk length filer, but that was implemented to remove the possible of section headers being a single chunk as they did not have retrievable content.**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI: I gave Claude my list of documents, including source, description, and URL, my chunking strategy, and my architecture table, and asked it to implement a script that would load all of my .txt files using open() and .read(), cleans them, and chunks them using the text splitter.*
- *What it produced: It produced a .py file that loaded all of the documents in the /documents directory and opened them with open() and .read() and attached the relative metadata. The script also cleaned the text before splitting and chunked the documents.*
- *What I changed or overrode: I had to change the location of the documents as Claude was not aware of where my .txt files were located and I had to add in a few debugging statements to ensure that the code was working properly when the python commands were run in the terminal.*

**Instance 2**

- *What I gave the AI: I gave Claude my retrival stage of the pipleine and my architecture table and asked it to implement code that would embed all of the chunks from the document ingestion step using sentence transformers and store them in ChromeDB with source metadata. Along with that, I asked it to implement a retrieve() function that would take in a query string and return the top 5 chunks along with the source.*
- *What it produced: Claude produced a script that embedded al of the chunks and stored them in ChromaDB with all of the source metadata. It also implemented the retrieve() function that takes in any query string and embeds it with the same model to return the top 5 chunks and the distance to show whether the chunks were similar or not.*
- *What I changed or overrode: I did not need to change anything for this instance.*
