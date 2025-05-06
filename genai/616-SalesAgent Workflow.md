# Introduction

Welcome to the **SalesAgent** implementation guide. In this guide, we will build an advanced question-answering agent (the "SalesAgent") that can answer user queries by searching for relevant information and reasoning over it. We will use a combination of powerful technologies to achieve this:

- **LangGraph** – to define a workflow graph for the agent's logic, including decision nodes and loops.
- **TavilyClient** – to perform live web searches and retrieve content for contextual augmentation.
- **Streamlit** – to create an interactive web UI where users can ask questions and get answers.
- **LangChain PromptTemplates** – to design robust prompts for the language model, especially for validating retrieval results and generating answers.

We will go step-by-step, with **detailed explanations and code examples** suitable for advanced developers. By the end, you will have a working SalesAgent system and a deep understanding of how each component works.

**Overview of the SalesAgent system:** The SalesAgent will take a user’s question, search for relevant information on the web (using Tavily), decide if the found information is sufficient (using an LLM validation step), possibly loop to search again with refined queries, and finally generate a well-informed answer. All these steps are orchestrated using a LangGraph workflow. This approach is a form of Retrieval-Augmented Generation (RAG), enhanced with a feedback loop: if the first retrieval doesn't yield an answer, the agent can try again with a better query ([LangGraph](https://blog.langchain.dev/langgraph/#:~:text=An%20example%20of%20why%20this,running%20an%20LLM%20in%20a)). Such cycles make the application more flexible and effective for complex queries.

**Technologies Used and Their Roles:**

- _LangGraph:_ A library that models agent workflows as graphs of nodes and edges. It lets us define a shared state (information that persists across steps), node functions (which perform tasks like calling an API or LLM), and edges that determine the next step in the workflow. Unlike a linear chain, LangGraph supports loops and conditional branching, which is perfect for our agent’s iterative search strategy. In short, **nodes do the work, and edges decide what to do next** ([LangGraph Glossary](https://langchain-ai.github.io/langgraph/concepts/low_level/#:~:text=1,BaseModel)) ([LangGraph Glossary](https://langchain-ai.github.io/langgraph/concepts/low_level/#:~:text=By%20composing%20,just%20good%20ol%27%20Python%20code)).

- _TavilyClient:_ An AI-tailored search engine API that provides real-time, factual web results for LLMs ([Tavily Search | ️ LangChain](https://python.langchain.com/docs/integrations/tools/tavily_search/#:~:text=Tavily%27s%20Search%20API%20is%20a,and%20factual%20results%20at%20speed)). We'll use Tavily to fetch relevant web pages or snippets related to the user's query. The retrieved content will serve as external knowledge that our LLM can use to formulate accurate answers (this is the "retrieval" in retrieval-augmented generation).

- _Streamlit:_ A Python framework for building web apps with minimal code. Streamlit will allow us to create a simple interface with input boxes and buttons so that users can interact with the SalesAgent. Streamlit makes it easy to add interactivity (text inputs, buttons, etc.) directly into our app ([Input widgets - Streamlit Docs](https://docs.streamlit.io/develop/api-reference/widgets#:~:text=Input%20widgets%20,sliders%2C%20text%20inputs%2C%20and%20more)), and we'll use it to display the agent’s responses in real time.

- _LangChain PromptTemplates:_ LangChain provides utilities for prompt engineering, such as **PromptTemplate** classes and **OutputParsers**. We will use these to craft the prompts given to the LLM in our agent. Specifically, we'll design prompt templates for two crucial steps: (a) **Retrieval validation**, where the LLM will examine search results and decide if more information is needed, and (b) **Question answering**, where the LLM generates the final answer using all available information. Using LangChain’s prompt tools will help ensure the LLM’s output is in the format we expect (for example, JSON for the validation step) and that it follows our instructions closely ([Prompt Templates | 🦜️ LangChain](https://python.langchain.com/docs/concepts/prompt_templates/#:~:text=Prompt%20templates%20help%20to%20translate,to%20guide%20a%20model%27s%20response)).

**Setting up the Development Environment:** Before diving into coding, make sure you have a suitable Python environment ready. You should have Python 3.8+ installed. We recommend creating a new virtual environment for this project. Then, install the required packages:

```bash
pip install langchain langchain-community langgraph tavily-python streamlit python-dotenv
```

Here's what each package is for:

- `langgraph` – LangChain’s LangGraph module (for building graph workflows).
- `langchain-community` – contains community-contributed tools like Tavily integration (optional if using LangChain’s wrapper).
- `tavily-python` – the Tavily API Python client.
- `streamlit` – for the web interface.
- `python-dotenv` – to load API keys from a `.env` file for security.

You will need API keys for any LLM service (e.g., OpenAI) and for Tavily. Sign up for Tavily to get an API key. Also ensure you have an OpenAI API key (if using OpenAI's models) or any other LLM provider key.

We'll use a **`.env` file** to store keys (like `TAVILY_API_KEY` and `OPENAI_API_KEY`) so we don't hardcode secrets in our code. The `python-dotenv` library will allow our script to load these at runtime. For example, your `.env` might contain:

```
TAVILY_API_KEY = your-tavily-key-here
OPENAI_API_KEY = your-openai-key-here
```

Using environment variables for keys is a best practice to keep credentials secure ([Tavily Search | ️ LangChain](https://python.langchain.com/docs/integrations/tools/tavily_search/#:~:text=We%20also%20need%20to%20set,site%20and%20creating%20an%20account)). In our code, we'll load these and use them when initializing the Tavily client and the OpenAI LLM.

With the environment set up and packages installed, you're ready to build the SalesAgent step by step.

---

# Understanding LangGraph

Before implementing the agent, it’s crucial to understand how **LangGraph** structures an LLM workflow. LangGraph allows us to define an execution graph consisting of **state**, **nodes**, and **edges**:

- **State**: A shared data structure that holds information persistent across the workflow. In LangGraph, state is often defined as a `TypedDict` or a Pydantic model, specifying the fields we'll track ([LangGraph Glossary](https://langchain-ai.github.io/langgraph/concepts/low_level/#:~:text=1,BaseModel)). For our SalesAgent, the state will include things like the user's query, search results, and the final answer (as well as any intermediate flags we need for logic).

- **Nodes**: Units of work (Python functions) that take the current state, perform some operation, and return an updated state ([LangGraph Glossary](https://langchain-ai.github.io/langgraph/concepts/low_level/#:~:text=2,State)). A node could call an API, run an LLM prompt, manipulate data, etc. In our agent, different nodes will handle searching, validating, and answering.

- **Edges**: Connections between nodes that determine which node runs next. Edges can be simple linear transitions or **conditional** based on the state ([LangGraph Glossary](https://langchain-ai.github.io/langgraph/concepts/low_level/#:~:text=3,conditional%20branches%20or%20fixed%20transitions)). Conditional edges allow branching logic: the next node can depend on the outcome of the previous node’s work (for example, go back to search if the answer wasn't found, or proceed to answering if it was).

LangGraph essentially lets us create a directed graph (which can have loops) representing the control flow of our agent. This is more flexible than a linear chain, enabling complex behaviors like iterative searching. _In short: nodes do the work, edges decide where to go next in the graph_ ([LangGraph Glossary](https://langchain-ai.github.io/langgraph/concepts/low_level/#:~:text=Python%20functions%20,just%20good%20ol%27%20Python%20code)).

## Defining the Graph State with TypedDict

Let's start by defining our **GraphState** using a `TypedDict`. This state will carry all the information through the workflow. We anticipate needing the following fields:

- `user_query`: str – the question asked by the user.
- `search_results`: list – the results returned from Tavily (could be a list of content snippets or a structured result).
- `needs_search`: bool – a flag from the validation step indicating if another search is needed.
- `refine_query`: str – a potentially refined search query suggested by the LLM (if the first search was not sufficient).
- `final_answer`: str – the answer generated by the agent.

We'll define this as a TypedDict for clarity and type-checking:

```python
from typing import List, TypedDict, Optional, Any

class GraphState(TypedDict):
    user_query: str
    search_results: List[Any]         # will hold raw search results (dicts from Tavily)
    needs_search: bool
    refine_query: Optional[str]
    final_answer: Optional[str]
```

A few notes:

- `search_results` is a list of `Any` because we will store Tavily's result objects (each might be a dict with keys like 'title', 'content', etc.).
- We initialize `refine_query` and `final_answer` as `None` (or Optional) since they may not be set until later in the workflow.

We will initialize the state when a query comes in (in the Streamlit interface or a function) with at least `user_query` set and other fields maybe defaulted (e.g., `needs_search = True` initially to trigger a search).

## Creating Nodes for the Workflow

Each step in our agent will be a node function. We foresee these main nodes:

1. **Search Node** – uses TavilyClient to search for the user's query (or a refined query) and updates `search_results`.
2. **Validate Node** – uses an LLM to analyze the results and decide if we need another search. It sets `needs_search` (True/False) and possibly `refine_query` (a better query if needed).
3. **Answer Node** – uses an LLM to generate the final answer from the query and available context (search results), and stores `final_answer` in the state.

Let's sketch what each node might look like in code (we will fill in details in later sections):

```python
# Pseudo-code structure for nodes, actual implementation will come later:
def node_search(state: GraphState) -> GraphState:
    query = state.get("user_query") if state.get("refine_query") is None else state.get("refine_query")
    # Call Tavily search API (implementation in next section)
    results = tavily_client.search(query, max_results=5, search_depth="advanced", include_raw_content=True)
    # Update state
    state["search_results"] = results.get("results", [])
    return state

def node_validate(state: GraphState) -> GraphState:
    # Examine state["search_results"] using LLM (implementation in later section)
    # Decide if more search needed, possibly get a refined query
    decision = validate_with_llm(state["user_query"], state["search_results"])
    # 'decision' could be a dict like {"need_search": bool, "refine_query": str or None}
    state["needs_search"] = decision["need_search"]
    state["refine_query"] = decision.get("refine_query")
    return state

def node_answer(state: GraphState) -> GraphState:
    # Use LLM to generate answer from state["search_results"]
    answer = answer_with_llm(state["user_query"], state["search_results"])
    state["final_answer"] = answer
    return state
```

Each node is a function that takes the current state (as a parameter or via closure) and returns an updated state dictionary.

Notice that `node_search` decides which query to use: initially the user's query, but if a `refine_query` is provided by the validation step, it will use that (meaning the LLM suggested a better query to try). This allows iterative refinement.

We will implement `validate_with_llm` and `answer_with_llm` using LangChain prompt templates later. For now, think of them as helper functions that call an LLM with a specific prompt and return either a decision or an answer.

## Adding Nodes and Conditional Edges to the Graph

With nodes defined, we need to connect them in a graph. We use **StateGraph** from LangGraph to build this workflow. First, we initialize a `StateGraph` with our `GraphState` type:

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(GraphState)
```

Now, let's add our nodes to this graph:

```python
# Adding nodes (name, function)
graph.add_node("search", node_search)
graph.add_node("validate", node_validate)
graph.add_node("answer", node_answer)
```

We also have special markers `START` and `END` available from LangGraph which represent the graph’s start and termination. By default, `START` is where the execution begins (unless we set a different entry), and `END` is a pseudo-node to indicate completion.

Next, we define edges. **Unconditional edges** are straightforward: one node flows directly into the next. In our case, after a search we always want to validate, so we add an edge from `"search"` to `"validate"`:

```python
graph.add_edge("search", "validate")
```

Now comes the crucial part: the **conditional edge** after validation. Based on the `needs_search` flag, we want either to loop back to search (if more info is needed) or proceed to the final answer. LangGraph supports conditional transitions by evaluating a function on the state or by mapping a node's output to specific next nodes ([LangGraph: Conditional Edge and Loop Explained | by Kamal Dhungana | GoPenAI](https://blog.gopenai.com/conditional-edge-and-cycle-in-langgraph-explained-da4a112bf1ea#:~:text=In%20LangGraph%2C%20a%20conditional%20edge,decision%20revisiting%20in%20LLM%20applications)).

One approach is to use a _router function_ and the `add_conditional_edges` method. The router function will inspect the state and return the name of the next node. For example:

```python
def route_after_validation(state: GraphState) -> str:
    # If validation says we need another search, go to "search"; otherwise, go to "answer"
    if state.get("needs_search"):
        return "search"
    else:
        return "answer"
```

Now we attach this conditional logic to the graph edges. We want to route from the `"validate"` node based on the `route_after_validation` function:

```python
graph.add_conditional_edges("validate", route_after_validation, {
    "search": "search",
    "answer": "answer"
})
```

This tells LangGraph: when leaving the `"validate"` node, call `route_after_validation(state)`. If it returns `"search"`, go to the node named `"search"`; if it returns `"answer"`, go to node `"answer"`. We provide a mapping of possible outputs to actual node names. (LangGraph will also handle if a node name like `"__end__"` is returned, to stop the graph, but here we explicitly route to `"answer"` which will eventually go to END.)

Under the hood, the conditional edge allows dynamic transitions based on runtime data, enabling loops in the graph (going back to search) ([LangGraph: Conditional Edge and Loop Explained | by Kamal Dhungana | GoPenAI](https://blog.gopenai.com/conditional-edge-and-cycle-in-langgraph-explained-da4a112bf1ea#:~:text=In%20LangGraph%2C%20a%20conditional%20edge,decision%20revisiting%20in%20LLM%20applications)) ([LangGraph: Conditional Edge and Loop Explained | by Kamal Dhungana | GoPenAI](https://blog.gopenai.com/conditional-edge-and-cycle-in-langgraph-explained-da4a112bf1ea#:~:text=dynamic%20paths%20through%20the%20graph,decision%20revisiting%20in%20LLM%20applications)). This is how our agent can perform multiple search-validate cycles if needed. The shared state (GraphState) makes this possible by carrying over data between iterations.

Finally, we add an edge from `"answer"` to the end of the graph:

```python
graph.add_edge("answer", END)
```

This means once the answer node has executed, the workflow terminates.

We should also specify the entry point of the graph (where execution starts). By default, if we added an edge from `START` to a node it would start there, but we can also set it explicitly:

```python
graph.set_entry_point("search")
```

(Alternatively, doing `graph.add_edge(START, "search")` achieves the same.)

At this point, our workflow graph structure is defined: **START → search → validate → (conditional: search or answer) → END**. This is a cyclical graph with a potential loop between validate and search, governed by the LLM’s decision.

## Compiling and Visualizing the Workflow

After defining nodes and edges, LangGraph requires you to **compile the graph**. Compilation prepares the graph for execution (it does validations, sets up internal structures, etc.) ([Introduction to LangGraph](https://mojtabamaleki.hashnode.dev/introduction-to-langgraph#:~:text=,HumanMessage)). We do this by calling:

```python
compiled_graph = graph.compile()
```

The `compiled_graph` is now a runnable object. We can invoke it by passing an initial state.

For instance, if we have `initial_state = {"user_query": "What is the revenue of Company X in 2023?"}` (and other keys as needed, possibly defaulting `needs_search=True`), we could do `result_state = compiled_graph.invoke(initial_state)` or simply `compiled_graph(initial_state)` to execute the workflow. The result will be a state dict containing the final answers.

LangGraph also provides ways to **visualize** the graph structure for debugging or documentation. One convenient method is converting the graph to a **Mermaid** diagram (Mermaid is a text-based format for drawing flowcharts). We can do:

```python
mermaid_code = graph.get_graph().draw_mermaid()
print(mermaid_code)
```

This will output a Mermaid flowchart description of our graph ([How to visualize your graph](https://langchain-ai.github.io/langgraph/how-tos/visualization/#:~:text=Mermaid%C2%B6)), which might look like:

```
graph TD;
 START --> search;
 search --> validate;
 validate -->|needs_search True| search;
 validate -->|needs_search False| answer;
 answer --> END;
```

This textual diagram shows the nodes and conditional branching (with the condition labeled for clarity). You can take this Mermaid code and render it (using Mermaid Preview or an online tool) to get a visual graph. LangGraph even has utilities to directly generate an image via Mermaid or Graphviz if needed, but since image embedding is disabled here, we stick to the textual representation. The key point is that **LangGraph's workflow can be visualized**, which helps ensure our logic is correct.

To summarize this section:

- We created a **GraphState** to hold our data.
- We defined node functions for each step of the agent.
- We added nodes to a StateGraph and connected them with edges, using `add_conditional_edges` for the branch/loop.
- We compiled the graph and saw how to visualize it in Mermaid.

Now that we have the skeleton of the agent's logic, let's implement the core functionality of each node, starting with retrieval using Tavily.

---

# Implementing Retrieval with TavilyClient

The first step in our SalesAgent workflow is retrieving relevant information for the user's query. We’ll use **TavilyClient** for this purpose. Tavily is a search API designed for AI agents – it provides web search results that include not just links, but also extracted content and even direct answers in some cases ([Python - Tavily Docs](https://docs.tavily.com/sdk/reference/python#:~:text=%60results%20%60%60list,query%2C%20generated%20by%20an%20LLM)). This is extremely useful for building an agent because it saves us from writing our own web scraping and it tailors results for use with LLMs.

## Setting Up Tavily API Access

To use Tavily, you need an API key. If you haven’t already, sign up at Tavily's website to obtain a key. Once you have it, store it in your `.env` file as `TAVILY_API_KEY`. We will load it in our code using `dotenv`:

```python
import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()  # load variables from .env
api_key = os.getenv("TAVILY_API_KEY")
if api_key is None:
    raise RuntimeError("TAVILY_API_KEY not set. Please add it to your .env file.")
```

Here, we make sure the API key is present. We then initialize the Tavily client:

```python
tavily_client = TavilyClient(api_key=api_key)
```

This client will be used to perform searches. (Note: Tavily offers both a search function and an extract function; here we are using the search which covers both finding relevant pages and extracting content from them.)

## Querying Tavily for Search Results

With the `tavily_client`, performing a search is straightforward. Tavily's `search()` method takes a query string and various optional parameters. For example:

```python
response = tavily_client.search(
    "Who is Leo Messi?",
    max_results=3,
    search_depth="advanced",
    include_answer="basic"
)
print(response)
```

The above (from Tavily's documentation) would return a JSON/dict response that might look like this:

```json
{
  "query": "who is Leo messi?",
  "follow_up_questions": null,
  "answer": "Lionel Messi, born in 1987, is an Argentine footballer ...",
  "images": [],
  "results": [
    {
      "title": "Lionel Messi Facts | Britannica",
      "url": "https://www.britannica.com/facts/Lionel-Messi",
      "content": "Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest ...",
      "score": 0.80917,
      "raw_content": null
    },
    {
      "title": "Lionel Messi Biography - Thefamouspeople",
      "url": "...",
      "content": "Lionel Messi has won multiple FIFA Ballon d'Or awards, numerous La Liga titles ...",
      "score": 0.57780,
      "raw_content": null
    },
    ...
  ]
}
```

Let's break down the Tavily response structure:

- **`query`**: Echoes the search query we asked.
- **`answer`** (optional): If `include_answer` is set, Tavily can return a quick answer generated from the results ([Python - Tavily Docs](https://docs.tavily.com/sdk/reference/python#:~:text=%60results%20%60%60list,query%2C%20generated%20by%20an%20LLM)) ([Python - Tavily Docs](https://docs.tavily.com/sdk/reference/python#:~:text=,winning%20seasons%20in%202009%20and)). (In our use-case, we might not rely on this, since we want our own LLM to formulate the answer with a custom prompt.)
- **`results`**: A list of search results. Each result typically has:
  - `title`: Title of the webpage.
  - `url`: URL of the result.
  - `content`: A snippet of the most relevant content from that page, as identified by Tavily's AI ([Python - Tavily Docs](https://docs.tavily.com/sdk/reference/python#:~:text=,content%20based%20on%20context%20quality)).
  - `score`: A relevance score (higher means more relevant).
  - `raw_content`: The full cleaned text of the page (if `include_raw_content=True` was passed). By default this is `None` unless requested, because it can be very large.

There are also fields like `images` (if images were requested) and `follow_up_questions` (Tavily might suggest related questions if applicable), but for our purposes, the main focus is the `results` list (and possibly `answer` field if we wanted a baseline answer).

For our SalesAgent, we will likely use `search_depth="advanced"` (to get a thorough search) and request `include_raw_content=True` for maximum context. However, including raw content for many results can be a lot of text, possibly too much for the LLM context window. An alternative is to use the `content` field, which is already a concise relevant snippet. We might strike a balance by using the `content` snippet for most purposes, and only retrieving full `raw_content` if needed for a top result.

Let's implement the **Search node (`node_search`)** properly with Tavily:

```python
import json

def node_search(state: GraphState) -> GraphState:
    # Determine the query to search for
    query = state.get("user_query")
    if state.get("refine_query"):
        # If a refined query is provided by the validation step, use it
        query = state["refine_query"]

    # Call Tavily search API
    try:
        response = tavily_client.search(
            query,
            max_results=5,              # retrieve up to 5 results
            search_depth="advanced",    # use advanced search for better accuracy
            include_raw_content=False   # we'll use the snippet content for now
        )
    except Exception as e:
        # Handle API errors (network issues, etc.)
        state["search_results"] = []
        print(f"Error during Tavily search: {e}")
        return state

    # The Tavily client returns a dict (or TavilyResponse object). Extract results list.
    results_list = response.get("results", [])
    state["search_results"] = results_list
    # We reset refine_query after using it to avoid sticky reuse (optional)
    state["refine_query"] = None
    # (We might also choose to reset needs_search here, but the validate node will set it anyway)
    return state
```

A few points in this code:

- We check if `state["refine_query"]` exists; if so, we use that for the search. Otherwise, we default to the original `user_query`.
- We call `tavily_client.search()` with certain parameters:
  - `max_results=5` to limit to top 5 results. You can adjust this as needed (Tavily allows up to 20, but more results = more text to process).
  - `search_depth="advanced"` for a deeper search. (Tavily's "basic" is faster but might be less comprehensive; "advanced" can dig deeper at the cost of slight delay.)
  - `include_raw_content=False` for now, meaning we rely on Tavily's `content` field. We can change this to True if we plan to feed raw content into the LLM, but that might be too verbose. Another strategy is to first use snippets for validation, and only if needed, fetch raw content of a specific URL. For simplicity, we won't do a second extraction step in this guide.
- We catch exceptions around the search call. In production, you'd want robust error handling (and perhaps retries) in case the API call fails or times out. Here we just log the error and set `search_results` to an empty list to allow the flow to continue gracefully.
- We put the results list into `state["search_results"]`. This could be a list of dictionaries as shown above. If the Tavily client returns a custom object, we might need to call something like `.to_dict()` or similar; but from the docs it seems to return a Python dict.
- We reset `refine_query` to None after using it, to avoid reusing the same refined query again in case of multiple loops (this is optional, depending on how we handle state in loops).

Now, after this node, our state will have `search_results` filled with potentially relevant information for the query. These will feed into the next step, validation.

## Processing and Structuring Retrieved Data

Now that we have search results, how do we use them? Typically, for context augmentation, we need to pass some representation of these results to the LLM in a prompt. There are a few ways to do this:

- **Pass raw text**: e.g., concatenate all the content snippets into one big context string. This is straightforward but could exceed token limits if there are many results or if they're long.
- **Select or summarize**: e.g., pick the top 1-3 results that seem most relevant (maybe by score or by checking if the content contains keywords from the question), or summarize each result's content to a shorter form.
- **Structured reference**: e.g., provide the LLM with a list of the result titles and snippets, perhaps with numbering, so the LLM knows there's multiple sources.

For the _validation_ step (deciding if more search is needed), we may not need the full content of each result – perhaps just the titles or a quick view of whether anything was found. But the LLM could potentially gauge the relevance of the results better if it sees some content.

For the _answer_ generation step, having the actual content is more important, since the answer should draw from it.

A practical approach:

- For **validation**, we can provide the LLM with the titles and maybe brief snippet of each result (to judge if the answer is likely in there).
- For **answering**, we provide the content of the top relevant results concatenated (with clear separators so the model knows the boundary between documents).

In code, after the search node, we might prepare a string summary of results for the next prompt. But since our nodes are separate, we might let the validate node itself handle formatting the input prompt from `state["search_results"]`.

However, it's good to structure the data now:
Let's say `search_results` is a list of dicts. We might create a helper to format them, for example:

```python
def format_results_for_prompt(results):
    """Format a list of search results into a string for LLM prompts."""
    if not results:
        return "No relevant information found."
    formatted = []
    for idx, res in enumerate(results, start=1):
        title = res.get("title", "Result")
        content = res.get("content", "")
        # Maybe truncate content to 200 characters for brevity in validation
        snippet = content[:200] + ("..." if len(content) > 200 else "")
        formatted.append(f"[{idx}] {title}: {snippet}")
    return "\n".join(formatted)
```

This will produce something like:

```
[1] Lionel Messi Facts | Britannica: Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest ...
[2] Lionel Messi Biography - Thefamouspeople: Lionel Messi has won multiple FIFA Ballon d'Or awards, numerous La Liga titles ...
...
```

for our example.

We can use this in the validation prompt to show the LLM what was found.

For the answer prompt, we might do a different formatting (maybe provide more content, and possibly the URLs or references if we want the model to cite sources).

At this stage, the key takeaway is that **Tavily has provided us with context data**. We have to incorporate that into our state and later prompts. The `search_results` in state is essentially our _retrieval memory_ for the query.

To recap this section:

- We configured the TavilyClient with our API key (using dotenv for security).
- We performed a search in the `node_search` function, retrieving up to 5 results with snippets.
- We stored these results in the state for downstream use.
- We discussed how to format and process the retrieved results for use in LLM prompts (though the actual usage will be implemented in the validation and answer nodes).

Next, we will build the **validation system**: using LangChain prompts to let the LLM analyze these search results and decide what to do next.

---

# Building a Validation System

After retrieving information, our agent needs to decide: **Do we have enough info to answer the question, or do we need to search again (perhaps with a refined query)?** This decision-making is what we call the **validation step**. We will implement this using an LLM, essentially asking the LLM to reason about the query and results.

Why use an LLM for validation? Because the LLM can understand the context of the question and gauge whether the snippets found are relevant or sufficient. It can also suggest how to improve the query if the results were off the mark. This is a form of meta-reasoning that makes the agent smarter.

We will use **LangChain's PromptTemplate** to create a robust prompt for this validation. We'll also leverage LangChain's output parsing to structure the LLM's response (we want a yes/no or instruction rather than a free-form answer here).

## Designing the Validation Prompt Template

The prompt to the LLM should clearly instruct it on what we expect:

- We will provide the **user's question**.
- We will provide a summary of the **search results** we got.
- We will ask the LLM to determine if the provided info is enough to answer the question.
- If it's not enough, we want the LLM to suggest a better search query or what to do next.
- The output should be in a structured format (like JSON) so our program can parse it easily.

Let's draft a prompt in plain language first:

_"You are an assistant helping to answer user questions. We have a question and some information found from a web search. Analyze whether the information is sufficient to fully answer the question. If it is sufficient, respond with an answer flag indicating no further search is needed. If it's not sufficient, suggest what to search for next (a refined query) to find the answer. Provide your response in a JSON format with fields for whether we need another search and the new query if applicable."_

We might include guidelines like "Only say we have enough if you are confident the info covers the question. If not, think of what missing piece or detail we should search for."

Now, to implement this with LangChain:
We can use `PromptTemplate` to insert the dynamic parts (question and search results summary).

First, format the search results. We can use the helper `format_results_for_prompt` we outlined. In the validate node, we might do:

```python
context = format_results_for_prompt(state["search_results"])
```

Now we create the prompt text:

```python
from langchain.prompts import PromptTemplate

validation_prompt = PromptTemplate(
    input_variables=["question", "results"],
    template=(
        "You are a smart assistant tasked with determining if we have enough information to answer a question.\n"
        "User Question: {question}\n"
        "Search Results:\n{results}\n\n"
        "Instructions: Analyze the above results and the question. If the information is sufficient to answer the question, output {{\"need_search\": false}}.\n"
        "If the information is NOT sufficient, output {{\"need_search\": true, \"refine_query\": \"<suggested new search query>\"}}.\n"
        "Only provide a JSON response with the keys 'need_search' and 'refine_query' (include 'refine_query' only if need_search is true). Do not add any extra explanation."
    )
)
```

In this template:

- `{question}` will be replaced by the actual user query.
- `{results}` will be replaced by the formatted results string.
- We explicitly instruct the assistant to output a JSON with `need_search` and optionally `refine_query`.
- We double curly brace `{{` in the template where we actually want a literal brace in the output (for JSON syntax in the instruction).

We have guided the LLM to either say:

```
{"need_search": false}
```

if it thinks the current info is enough, or:

```
{"need_search": true, "refine_query": "some new search terms"}
```

if more info is needed.

By constraining the output to JSON, we make it easy to parse programmatically. This approach uses **structured outputs** which is a known technique in LangChain to get multiple fields out of an LLM reliably ([Structured output parser | ️ LangChain](https://python.langchain.com/v0.1/docs/modules/model_io/output_parsers/types/structured/#:~:text=response_schemas%20%3D%20%5B%20ResponseSchema%28name%3D,%29%2C%20%5D%20output_parser)) ([Structured output parser | ️ LangChain](https://python.langchain.com/v0.1/docs/modules/model_io/output_parsers/types/structured/#:~:text=We%20now%20get%20a%20string,insert%20that%20into%20our%20prompt)).

We can even formalize the expected output format using LangChain's `ResponseSchema` and `StructuredOutputParser` for extra rigor:

```python
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

# Define the expected fields
schemas = [
    ResponseSchema(name="need_search", description="Whether another search is needed (true/false)"),
    ResponseSchema(name="refine_query", description="Suggested search query for next step if need_search is true")
]
output_parser = StructuredOutputParser.from_response_schemas(schemas)
format_instructions = output_parser.get_format_instructions()
```

We could incorporate `format_instructions` into our prompt template instead of manually writing JSON instructions. However, since we already custom-wrote the JSON instruction, either approach works. Using `output_parser` is more systematic, but we'll stick to our manual instruction for clarity.

## Implementing the Validate Node with LLM

Now, let's code the `node_validate` function using the prompt above. We need an LLM model to call. We can use OpenAI's GPT-4 or GPT-3.5 via LangChain's `ChatOpenAI`, or any other model supported by LangChain. We'll assume an OpenAI key is set (via environment `OPENAI_API_KEY` loaded by dotenv).

```python
from langchain.chat_models import ChatOpenAI

# Initialize an LLM (for example, GPT-4 with temperature 0 for deterministic output)
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

def node_validate(state: GraphState) -> GraphState:
    question = state["user_query"]
    results = state.get("search_results", [])
    # Format the search results into a string for the prompt
    results_text = format_results_for_prompt(results)

    # Create the prompt from the template
    prompt_text = validation_prompt.format(question=question, results=results_text)

    # Run the LLM on the prompt
    try:
        llm_response = llm.predict(prompt_text)
    except Exception as e:
        # If LLM call fails, default to needing another search as safe fallback
        print(f"Error during validation LLM call: {e}")
        state["needs_search"] = False
        state["refine_query"] = None
        return state

    # Parse the response. We expect a JSON string.
    response_text = llm_response.strip()
    if not response_text:
        # Empty response, handle as no need to search (to avoid infinite loop)
        state["needs_search"] = False
        state["refine_query"] = None
        return state

    # Ensure it's valid JSON
    if response_text[0] != "{":
        # If the model gave some extra text before JSON, try to find the JSON part
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}')
        if start_idx != -1 and end_idx != -1:
            response_text = response_text[start_idx:end_idx+1]
    try:
        decision = json.loads(response_text)
    except json.JSONDecodeError:
        # If parsing fails, we can try to fix or just assume need_search true without refine (or set false to stop loop)
        print("Failed to parse JSON from LLM, got:", response_text)
        state["needs_search"] = False
        state["refine_query"] = None
        return state

    # Extract decision fields
    need_search = decision.get("need_search", False)
    refine_query = decision.get("refine_query", None)
    state["needs_search"] = need_search
    # Only set refine_query if need_search is true and a suggestion is given
    state["refine_query"] = refine_query if need_search else None

    return state
```

Let's explain this:

- We load `question` and `results` from the state.
- Use `format_results_for_prompt` to create `results_text` summarizing the search hits.
- Format the prompt using our `validation_prompt` template.
- Call the LLM with `llm.predict(prompt_text)`. (LangChain's `ChatOpenAI` can use `.predict()` for a single message prompt, since our prompt is a single combined string. Alternatively, we could structure it as a system/message in a chat format, but this straightforward way works given our prompt already contains instructions.)
- We set `temperature=0` on the model to minimize randomness – we want a clear, deterministic decision, not a creative answer.
- Error handling: If the LLM call fails (maybe due to rate limit or other issues), we handle it by defaulting `needs_search` to False (meaning proceed to answer to avoid being stuck) or we could default to True. There is a choice: defaulting to False ensures the agent doesn't loop forever if validation fails; defaulting to True might cause an extra search that might be unnecessary. We choose False with a note that it's a safe fallback to end the loop.
- We then strip the response and check if it exists. If it's empty, we also break the loop (set `needs_search = False`).
- We attempt to parse the LLM's output as JSON. Often, even with instructions, the model might include some explanation or formatting. We handle if there's text before or after the JSON braces by extracting the substring between the first `{` and the last `}`. This simple heuristic often gets the JSON portion.
- If JSON parsing still fails, we log the raw output for debugging and default to ending the loop (`needs_search=False`).
- If parsed successfully, we extract `need_search` (which should be True/False) and `refine_query` if present.
- We update the state accordingly:
  - `needs_search` gets set to the boolean.
  - `refine_query` is set only if another search is needed (True). If no further search is needed, we don't carry over any refine query (and likely it will be absent or None in the JSON anyway).

Now the `node_validate` will leave in the state a flag indicating whether to loop or not, and if looping, a new query to use.

This structured approach ensures we have a clear signal for the graph’s conditional edge:

- If `state["needs_search"]` is True, our `route_after_validation` will send us back to the `"search"` node.
- If False, we will proceed to `"answer"` node.

One more thing: We might want to limit how many loops can happen to avoid an infinite cycle if something goes wrong (for example, the LLM keeps saying search more but the searches don't yield new info). We can incorporate a counter in the state (like `iteration: int` count of search attempts) and break after e.g. 2 or 3 iterations. To keep things simpler, we'll not add it explicitly, but it's a good practice for production (we could add `iteration` to GraphState and increment in the validate node each time, and modify the router to go to answer if a max is reached regardless).

## Processing LLM Outputs and Reasoning

In the code above, we processed the LLM output by parsing JSON. This is an example of extracting structured information from the LLM's reasoning. We constrained the reasoning to an internal process (the model will think in the background per the prompt, but only output the JSON). We didn't explicitly ask the model to show its reasoning chain (like "let's think step by step") to avoid unnecessary verbosity in the output. However, such chain-of-thought prompting can be useful if we want the model to better reason before giving the final JSON. For advanced debugging, one might prompt the model to output a rationale and then the JSON, but then we'd have to parse out the rationale.

For clarity and consistency, we required _only JSON output_, making parsing straightforward.

**Why JSON?** Because it ensures our program can easily read the decision. By enforcing a specific structure, we avoid the model giving a long paragraph that we'd have to interpret with brittle logic. LangChain’s `StructuredOutputParser` basically automates this idea by adding format instructions and doing the JSON parsing for us ([Structured output parser | ️ LangChain](https://python.langchain.com/v0.1/docs/modules/model_io/output_parsers/types/structured/#:~:text=We%20now%20get%20a%20string,insert%20that%20into%20our%20prompt)). We manually implemented similar logic here.

If you inspect the model's behavior during this validation:

- It will look at the query and the snippets. For example, if the query is "What is the revenue of Company X in 2023?" and our search results are just generic info about Company X but nothing about revenue in 2023, the model might conclude `need_search: true` and suggest refining the query to "Company X 2023 revenue" or a similar more specific query.
- If the query is "Who is Lionel Messi?" and our results clearly have his bio and facts, the model will likely output `need_search: false`, meaning we have enough to answer (since the snippets contain relevant info about Messi).
- If the results are irrelevant or empty, the model might also output `need_search: true` with a suggestion to search differently.

This validation step is essentially adding a reasoning loop where the LLM helps improve its own input. It's a powerful pattern noted in the LangChain community, where an LLM in a loop can yield better results than a single-pass retrieval ([LangGraph](https://blog.langchain.dev/langgraph/#:~:text=An%20example%20of%20why%20this,running%20an%20LLM%20in%20a)).

## Structuring Responses with JSON Parsing

We touched on this above, but to emphasize: by structuring the LLM's response as JSON, we leverage a simple parse step (`json.loads`) to extract the needed values. This technique can be extended beyond just true/false flags:

- We could have the model output a rationale or an identified knowledge gap.
- We could include fields like `"confidence": 0-10` to gauge how confident it is the answer is present.
- We could output multiple possible refine queries or categorize the type of answer needed.

For our needs, just the boolean and one optional query string suffice.

LangChain's output parser utilities provide a robust way to enforce this. If we had used `StructuredOutputParser` with the `schemas` defined, our prompt would have included something like:

```
format_instructions = output_parser.get_format_instructions()
```

This `format_instructions` might look like:
_"The output should be a JSON object with two keys: 'answer' and 'source' ..."_ (in an example from docs ([Structured output parser | ️ LangChain](https://python.langchain.com/v0.1/docs/modules/model_io/output_parsers/types/structured/#:~:text=We%20now%20get%20a%20string,insert%20that%20into%20our%20prompt))). In our case it would instruct keys 'need_search' and 'refine_query'. We could append that to the prompt for a more model-agnostic way. Nonetheless, our approach is fine and we've manually handled possible deviations.

Now, at the end of the validate node:

- If `needs_search` is true, the state carries a new query and the graph will loop to `node_search` again, which will use this `refine_query`.
- If `needs_search` is false, the graph moves forward to the answer node.

We have thus created a **validation system** that uses an LLM to ensure our retrieval is on track, making the SalesAgent more robust and accurate.

Next, let's focus on generating the final answer with the information we have.

---

# Enhancing Answer Generation

Once our agent has gathered (and possibly iteratively refined) the necessary information, it's time to produce the final answer for the user. This section covers how to design an effective prompt for answer generation, how to handle cases where information might still be incomplete, and how to optimize the quality of the LLM's response.

## Designing an Effective Answer Generation Prompt

The answer generation prompt is critical – it needs to provide the LLM with:

- The user's question.
- The relevant context information (from the search results).
- Instructions on how to format or structure the answer (if any specific requirements, such as "provide a concise answer" or "list sources").
- Any style guidelines (since this is a SalesAgent, perhaps the tone should be professional and helpful).

For our SalesAgent, let's assume we want a factual answer, possibly with a friendly tone as a sales assistant might have, but mostly we care about correctness and completeness. We might also want to avoid the LLM hallucinating or using information not found in the context.

A common pattern for RAG (Retrieval-Augmented Generation) prompts is:

```
Given the following context, answer the question.

Context:
{{context}}

Question: {{question}}

Answer:
```

And we instruct the model to only use the context to answer, or say if it doesn't know.

We can incorporate multiple snippets of context. Since our `state["search_results"]` is a list of results (with snippet content, and optionally raw content if we fetched it), we need to decide how to present it. If the snippets are short and relevant, we could just concatenate them. If they are longer, we might include only the top 1-3.

Perhaps we take the top 3 results content. Alternatively, if one result is clearly the best, we could focus on that. For simplicity, let's include the content from all results but with clear separators.

We could format context like:

```
[Source 1] {content from result 1}
[Source 2] {content from result 2}
...
```

This labeling could help if we wanted to reference sources, but the prompt didn't explicitly ask to output sources. The user didn't specify they want citations in the answer. However, since this is an advanced guide, we might mention that as an option.

Let's design a prompt template:

```python
answer_prompt_template = """
You are a knowledgeable assistant helping answer a user's question using the provided context.
If the answer is not directly in the context, do your best to infer from it, but do not fabricate details.

User Question: "{question}"

Context:
{context}

Your task: Provide a clear and concise answer to the user's question.
If the context is insufficient to answer, say "I'm sorry, I don't have that information."
Otherwise, base your answer only on the given context. Do not include information not in the context.

Answer:
"""
```

Points about this prompt:

- We restate the question and provide the context.
- We instruct the assistant not to fabricate (to reduce hallucination) and to stick to context.
- We give a fallback instruction: if not enough info, apologize and say you don't have the info. (This is one way to handle missing information gracefully.)
- We explicitly say the answer should be clear and concise. We could tailor this to the style needed (e.g., if this was a sales scenario, maybe "persuasive" or "customer-friendly tone", but let's keep it straightforward).
- We did not ask for sources in the output, but we could. For example, some applications require the answer to cite which sources it used. We could add: "Include the source number in parentheses for each fact." However, the prompt didn't explicitly request that, so we'll keep it simple.

If needed, one could modify the prompt to produce an answer along with references (like "According to [Source 1], ...").

We will feed this prompt to the LLM along with the context from our state.

## Handling Missing Information Retrieval

It is possible that even after our validation loops, the context we have is not enough to answer the question. This could happen if:

- The needed info isn't on the web (or at least not found by Tavily).
- The refine loop gave up after a certain number of tries.
- The LLM misjudged and stopped searching too early.
- Or maybe the question is out of scope.

We partially addressed this by instructing the LLM to respond with an apology if context is insufficient. This way, the user gets a proper acknowledgement instead of a made-up answer.

Additionally, our validation step tries to ensure sufficiency. If it worked well, by the time we reach answer generation, ideally `needs_search` was false because the model believed the info is enough.

However, just in case, we double-handle: in the answer prompt, "If the context is insufficient to answer, say you don't have that information." This is an extra safety net.

We might also consider if `state["search_results"]` is empty (meaning Tavily found nothing at all). In such case, we can short-circuit: Instead of even calling the LLM for answer, just return "I'm sorry, I couldn't find any information on that." This check can be in the answer node code:

```python
if not state["search_results"]:
    state["final_answer"] = "I'm sorry, I don't have that information."
    return state
```

This prevents asking the model with no context (where it might then guess or hallucinate).

Another scenario: The model might have partial info and could still attempt an answer that is not fully correct. Our instructions discourage fabrication, but it might still try to "be helpful" by guessing. Using a low temperature (0 or near 0) helps in that it will stick to the given content and not wander too creatively.

## Optimizing LLM Response Quality

Quality of the final answer can depend on a few factors:

- **Model Choice**: GPT-4 tends to give better, more detailed answers than GPT-3.5, albeit slower and costlier. For a sales agent application, quality might trump speed, so GPT-4 is a good choice if available. We used `"gpt-4"` in the validate step; we'll do the same for answer. If only GPT-3.5 is available, it can still work, but you might need to adjust prompts or accept slightly more risk of error.
- **Temperature**: We likely want a factual answer, so keeping temperature low (0 to 0.3) is wise. This reduces randomness and keeps the answer focused on context.
- **Prompt Clarity**: The instructions should unambiguously tell the model what to do and not do. We have tried to make it clear (no outside info, apologize if not enough).
- **Context Relevance**: If we feed irrelevant or too much context, the model might get confused or include irrelevant details. It's important to only include context that we think is helpful. Our retrieval step already tries to get relevant content; we might further filter it:
  - For example, if we had 5 results but only the first two seem on-topic, we could include only those two in the context to avoid distraction from off-topic snippets.
  - We could do a quick check: does the snippet contain keywords from the question? If not, maybe skip it.
  - For advanced usage, one might vector-embed the question and snippets to check similarity, but that's beyond scope here.
- **Length Control**: We might want to ensure the answer isn't too long or too short. We didn't explicitly instruct length, except "concise". If needed, we could add "Answer in a single paragraph." or "Answer in at most 5 sentences." depending on requirements.

Given this, let's implement the **Answer node (`node_answer`)**:

```python
answer_prompt = PromptTemplate(
    input_variables=["question", "context"],
    template=(
        "You are a knowledgeable assistant helping answer a user's question using the provided context.\n"
        "User Question: \"{question}\"\n"
        "Context:\n{context}\n"
        "Instructions: Provide a clear and concise answer to the user's question based only on the context above.\n"
        "If the context does not contain the answer, say \"I'm sorry, I don't have that information.\".\n"
        "Do not include information not found in the context. Do not cite the sources in the answer, just give the answer.\n"
        "\nAnswer:"
    )
)

def node_answer(state: GraphState) -> GraphState:
    question = state["user_query"]
    results = state.get("search_results", [])
    # Short-circuit if no results at all
    if not results:
        state["final_answer"] = "I'm sorry, I don't have that information."
        return state
    # Prepare context text by concatenating snippets (limit content length if needed)
    context_parts = []
    for res in results:
        content = res.get("content") or res.get("raw_content") or ""
        if content:
            context_parts.append(content.strip())
    # If content is too long, truncate or take top N
    # Here, take first 3 results content as context for example
    context = "\n\n".join(context_parts[:3])

    # Format prompt
    prompt_text = answer_prompt.format(question=question, context=context)
    try:
        answer = llm.predict(prompt_text)  # using the same llm (ChatOpenAI) initialized earlier
    except Exception as e:
        print(f"Error during answer LLM call: {e}")
        # Fallback
        state["final_answer"] = "I'm sorry, I cannot generate an answer at the moment."
        return state
    # Strip any leading/trailing whitespace/newlines
    answer = answer.strip()
    state["final_answer"] = answer
    return state
```

Explanation:

- If `results` is empty, we immediately set an apologetic message and return.
- We build the `context` by extracting the `content` from each result. We prefer `content` (the relevant snippet). If for some reason `content` is empty but `raw_content` is available, we use that (though raw_content might be very long).
- We join the context from the first 3 results separated by blank lines. (3 is arbitrary here; depending on your data, you might include all if short, or just top 1 if it's clearly the answer.)
- We format the prompt with question and context.
- We call the LLM to get the answer.
- We handle errors gracefully by giving a fallback message.
- We strip the answer of extra whitespace and save it in `state["final_answer"]`.

By asking the model to answer "based only on the context above", we aim to ground the answer in facts we found. The model, if it follows instructions, will avoid adding unknown info. The line about apologizing if not in context ensures that if, for example, our context didn't actually contain an answer, the model won't hallucinate one but rather say it can't find it. This behavior aligns with the principle of not guessing when knowledge is lacking – important for trustworthiness, especially in domains like sales where incorrect info can be problematic.

This completes the logic of our SalesAgent's core loop:

1. Search (collect info).
2. Validate (decide to search more or not).
3. Possibly loop back to search with refined query.
4. Answer (use the info to answer question).

Next, we’ll integrate this with a Streamlit UI so users can interact with it in real time.

---

# Creating an Interactive UI with Streamlit

Now that the SalesAgent logic is implemented, we want to make it accessible through a user-friendly interface. **Streamlit** is an excellent choice for quickly turning a Python script into a web app with interactive widgets, without dealing with front-end code.

In this section, we’ll build a simple Streamlit app that allows a user to enter a question and then see the agent’s answer (and possibly some intermediate info if we choose to display it).

## Designing Input and Output Interfaces

For our SalesAgent UI, the key components are:

- A text input field where the user types their question.
- A button to submit the question and run the agent.
- An area to display the answer returned by the agent.
- (Optionally) We could also display the search results or the reasoning, for transparency or debugging, but since this is for end-users (sales or customers), we might hide that detail. For development, you could show it.

With Streamlit, we can achieve this in a few lines:

```python
import streamlit as st

# Title or header for the app
st.title("SalesAgent Q&A System")

# Text input for user query
user_query = st.text_input("Enter your question:", "")

# When button is clicked, run the agent
if st.button("Get Answer"):
    if user_query.strip() == "":
        st.write("Please enter a question.")
    else:
        # Call our LangGraph workflow with the user query
        initial_state = {
            "user_query": user_query,
            "search_results": [],
            "needs_search": True,
            "refine_query": None,
            "final_answer": None
        }
        with st.spinner("Searching for answers..."):
            result_state = compiled_graph.invoke(initial_state)
        # Once done, retrieve the answer from state
        answer = result_state.get("final_answer")
        if answer:
            st.markdown("**Answer:** " + answer)
        else:
            st.markdown("**Answer:** I'm sorry, I couldn't find an answer.")
```

Let's break this down:

- `st.title` sets a nice title at the top of the app.
- `st.text_input` creates a text box for input. We provide a label "Enter your question:". The second argument `""` is the default value (empty). This returns whatever the user types as `user_query`.
- `st.button("Get Answer")` creates a clickable button. Streamlit works such that when you click the button, it causes the script to rerun and the condition `if st.button(...):` becomes True on that run. We check if the user input is not empty, otherwise prompt to enter a question.
- We then prepare an `initial_state` for our graph. We ensure all fields of GraphState are present. `needs_search` starts as True to trigger at least one search.
- We use a context manager `st.spinner("...")` to show a message while the computation is happening (useful because LLM calls and web searches take a few seconds, and we want the user to know it's working).
- We call `compiled_graph.invoke(initial_state)` to run the workflow. Alternatively, `compiled_graph(initial_state)` might also work if `StateGraph` supports `__call__`. We'll use `.invoke()` for clarity. This runs through the nodes and edges we set up, including any loops, until completion.
- The result is a final state. We extract `final_answer` from it.
- We then display the answer with `st.markdown`. We bold the word "Answer:" and append the answer text. Using markdown allows rendering any formatting in the answer (if the answer contained markdown or needed formatting, but usually it'll be plain text).
- If for some reason `final_answer` is None, we default to an apology message.

This simple UI does the job. The user enters a question and clicks the button, then sees the answer.

## Handling User Interactions with Streamlit Widgets

The above code already covers the main interaction:

- `st.text_input` handles user input.
- `st.button` triggers the processing.

We should note a couple of Streamlit behaviors:

- Streamlit runs top to bottom on each interaction (initial page load, and then on each widget interaction).
- The values of `user_query` and the state of `st.button` are reset each run. However, `st.button` returns True only on the exact run when the button was clicked. After that, on the next rerun, it will be False again (unless clicked again).
- We use `with st.spinner():` to give feedback. This is optional but improves UX.

For a slightly more refined interface, we could:

- Use `st.text_area` instead of `st.text_input` if we expect long questions or want multiline input (like a description of a problem).
- Display intermediate info. For example, we could show the search results or the refine query the agent came up with, in an expander or hidden behind a toggle for those interested. For example:
  ```python
  with st.expander("Search results details"):
      for res in result_state.get("search_results", []):
          st.write(f"- {res.get('title')}: {res.get('content')[:100]}...")
  ```
  This would list the titles and first 100 chars of each result found. This could be interesting for a developer or power user to see where info came from.
- Show if the agent had to do multiple search rounds. We could count rounds by adding an `iteration` in state or by checking if `refine_query` was used. Perhaps, in the expander, note if a refine query was suggested: `if result_state.get("refine_query"): st.write("Refined query used: " + result_state["refine_query"])`. (After final state, refine_query might be left over from last validate if it didn't need it; in our logic, we clear refine_query when not needed.)
- We might also catch exceptions at a higher level. For instance, if `compiled_graph.invoke` throws an error (maybe due to a bug in nodes or an API call failing catastrophically), we should handle it so the Streamlit app doesn't crash. We could wrap it in try/except and display an error message via `st.error("An error occurred, please try again.")`.

Given the complexity we've managed, hopefully our nodes are robust enough.

## Running the Workflow and Displaying Results

When the user clicks the button:

1. `node_search` runs: calls Tavily API, gets results.
2. `node_validate` runs: calls LLM for validation.
   - If `needs_search` true, the graph goes back to `node_search` with a new `refine_query` in state, then validation again, etc.
   - If `needs_search` false, it goes to node_answer.
3. `node_answer` runs: calls LLM to generate answer.
4. Graph ends, returns final state.

This happens relatively quickly, but each API call can take time. Searching might take ~1-2 seconds, each LLM call (especially GPT-4) might take a few seconds. So total time could be, say 5-10 seconds for a query with one loop, more if multiple loops. The spinner informs the user to wait.

Once completed, the Streamlit app will show the answer. Because we used `st.markdown` for the answer, if the answer contains things like newlines, bullet points, etc., they will render nicely (markdown supports basic formatting). If it's plain text, it just shows as a paragraph.

We can enhance the display:

- Use `st.write` or `st.markdown` interchangeably; `st.markdown` is good for formatting.
- Possibly style the answer differently or show it in a text box. But bold "Answer:" label should suffice for clarity.
- We could also add an input for selecting which model to use or number of results, for experimentation. That might clutter the UI for end users though.

In summary, Streamlit makes it easy to wire up our pipeline to a web interface. With just a few widget functions, we have a working app:

- The user enters a query and hits a button.
- The agent runs under the hood (our LangGraph-directed process).
- The answer is displayed to the user on the same page.

This transforms our code from a backend script into an interactive tool that others can use.

Now that we have the UI set up, let's consider some optimizations and best practices to make this system robust and efficient.

---

# Optimizations and Best Practices

Building an advanced agent like this involves not just writing the code, but also ensuring it runs efficiently and handles errors gracefully. In this section, we'll discuss ways to improve performance, manage errors, and design the system for scale.

## Error Handling and Logging

**Error handling** is crucial because our agent depends on external services (Tavily API, OpenAI API). Things can go wrong: network issues, rate limits, invalid responses, etc. We've added try/except blocks around our API calls in the node functions to catch exceptions and prevent crashes. Here are some best practices:

- **Log errors**: Use Python's `logging` module or simple print statements (as we did) to record what went wrong. For example, if Tavily search fails, we logged the exception. In a production setting, integrate with a logging system or at least write to a file.
- **Graceful degradation**: If a search fails, perhaps try a fallback search (maybe using a different API or using a cached result if available). If an LLM call fails due to timeout, you might retry once or use a simpler model as fallback. In our code, we just stopped the loop if validation LLM failed or gave a default answer if answer LLM failed.
- **User feedback**: In the UI, if something goes wrong and we catch it, it's good to inform the user. Using `st.error("message")` can show a red error message. We might do this in the except block of the Streamlit interface if invoke fails. This prevents the user from waiting endlessly or getting no response. For example:
  ```python
  try:
      result_state = compiled_graph.invoke(initial_state)
  except Exception as e:
      st.error("Oops, something went wrong while processing your question. Please try again.")
      print(e)
      return
  ```
  This way, at least they know it didn't work that time.
- **Validation of outputs**: We attempted to parse JSON from the LLM. Sometimes the model might not follow instructions (especially if using a weaker model or if context confuses it). Our parsing logic trimmed to braces and tried `json.loads`. In more complex cases, LangChain's `OutputFixingParser` could be used to automatically attempt to correct minor JSON format issues ([Structured output parser - ️ LangChain](https://python.langchain.com/v0.1/docs/modules/model_io/output_parsers/types/structured/#:~:text=This%20output%20parser%20can%20be,for%20less%20powerful%20models)), or we could re-prompt the model: "Your output was not valid JSON, please output only JSON." if initial parse fails.
- **Prevent infinite loops**: It's possible (though we tried to avoid it) that the LLM might consistently say `need_search: true` but each refine query doesn't yield the answer, or it toggles back and forth. Without a safeguard, the agent could loop indefinitely. It's wise to have a loop counter in the state (e.g., `state["iteration"] += 1` in validate) and break after some attempts. For example, if `iteration >= 3`, set `needs_search=False` to stop. This ensures the agent gives up after a few tries and returns whatever it has (or a "can't find" answer). This is a practical limit to avoid runaway API calls and user waiting forever.

**Logging**:

- Use `logging` library with appropriate level (INFO, ERROR, DEBUG) to record events. You can configure logging to output to console or file.
- You can log the question asked, maybe log each refine query, and whether a second search was performed, etc. This is useful for monitoring how the agent is used and how well it's performing (in terms of requiring multiple searches or not).
- For deeper debugging, you might log the LLM's raw responses in validation to see what it thought. But be careful not to log sensitive info; if user questions are confidential, logs should be protected.

Additionally, consider integrating with LangChain's tracing tools. The snippet in LangChain docs mentioned `LANGSMITH_TRACING` environment variable ([Tavily Search | ️ LangChain](https://python.langchain.com/docs/integrations/tools/tavily_search/#:~:text=It%27s%20also%20helpful%20,class%20observability)). If set, it could record the chain of calls and results in LangSmith (LangChain's monitoring UI). This might or might not capture LangGraph flows, but it's something to explore.

## Performance Optimizations

Performance could be an issue since we involve multiple sequential calls:

- Web search API call(s)
- LLM calls (validate and answer, possibly multiple loops)

**Parallelizing**: If our workflow had independent branches or multiple tasks that could happen simultaneously, LangGraph could run them in parallel (since it's a graph). In our case, the steps are sequential (can't answer before search, etc.), so no obvious parallelism. But if, for instance, we had two different search strategies (web search and internal DB) we could run them in parallel as two nodes and then join results.
LangGraph supports parallel node execution in a super-step if they have no dependencies ([LangGraph Glossary](https://langchain-ai.github.io/langgraph/concepts/low_level/#:~:text=A%20super,no%20messages%20are%20in%20transit)), but our design is linear/looping.

**Caching**: One way to optimize is caching results of expensive operations. For example:

- Cache Tavily results for queries we've seen before (to avoid hitting the API again). If the app might get repeated questions, a simple dictionary or a more persistent cache (like a database or disk) could store the search results for a query. Next time, skip the API and use cached data if available and not stale.
- Cache LLM outputs for identical prompts. LangChain offers a cache mechanism that can store LLM responses for given prompts. If an identical validation scenario appears or the same final answer prompt, it could reuse it. In practice, identical prompts are less common (unless the same question is asked again).
- At least, caching the final answer for a given question is beneficial. That can be as simple as storing `user_query -> final_answer` in a dict or file. Then if `user_query` is seen again, just return the answer immediately. This is more useful if the agent is deployed for many users where questions might repeat (like FAQs).

**Reducing API calls**: We used one LLM call for validation and one for answer. We could consider saving one call by combining steps. Some designs have the LLM do the decision and answer in one prompt. For example:

- Ask the LLM: "Here's the question and context. If you can answer, give the answer. If not, suggest a refine query." and then check if it gave an answer or a suggestion. This would merge validation and answer generation into a single prompt. However, it complicates parsing (two possible outputs), and it might not be as reliable for multi-turn retrieval. We opted for two distinct prompts for clarity and modularity. For performance, two calls is fine, but if using GPT-4, that's two expensive calls per query. One could experiment with GPT-3.5 for validation (cheaper, and it's a simpler task) and GPT-4 for final answer (complex task), to cut cost/latency.

**Model selection**: Using a faster model (like gpt-3.5) can improve speed, though possibly at the cost of some accuracy or instruction-following. One could try using GPT-3.5 for validation with structured output (it should handle JSON output fine in most cases), and GPT-4 for the answer, or even GPT-3.5 for both if cost is a concern. It might occasionally hallucinate more, so additional prompt tuning or output checking might be needed. This is a trade-off depending on deployment needs.

**Streamlit performance**: For a single user, Streamlit is fine. But note that each user connecting to a Streamlit app runs a separate session (which runs the script separately). If multiple users use it concurrently, calls will multiply. This is not an issue unless heavy load. Streamlit is not asynchronous, so each request will hold some server compute. It's okay for moderate usage, but for heavy usage with many queries per second, a more scalable approach (like a FastAPI with async calls) might be needed. However, integrating LangGraph with an async framework would need careful handling of the async calls.

**Token limits**: Keep an eye on how large the context can get. If we included raw content of multiple pages, we could hit the model's token limit (which might be 4k or 8k tokens). We truncated to first 3 results. We might also truncate each snippet to, say, 500 characters (a few sentences) to avoid overload. This is a kind of optimization to ensure prompt size is manageable.

**Batching**: Not directly applicable here (we answer one question at a time), but if we needed to answer many questions in one go (like an offline batch process), we could consider batching prompts to the LLM if the API supports it. OpenAI API can do up to certain tokens, but usually one question per call is simpler.

## Scaling the Workflow for Larger Applications

If this SalesAgent were to be deployed company-wide or to many users, consider:

- **Deploying on a server/cloud**: Streamlit can be deployed on Streamlit Community Cloud (for smaller apps), or containerized to run on services like Heroku, AWS EC2, etc. If using Streamlit, each instance might handle a limited number of users. For more scalable architecture, one might expose the core logic as an API and have a separate frontend (or multiple frontends).
- **Multi-user data**: If multiple users ask simultaneously, thanks to Streamlit's session state, they won't interfere with each other (each has its own state and calls). But if we used any global variables for state or results cache, ensure to handle thread safety or use Streamlit's caching which is thread-safe.
- **Load management**: If expecting high traffic, you might implement rate limiting or queueing to avoid overloading the LLM API (since OpenAI etc., have rate limits per API key). Tools like FastAPI and Redis queue could throttle requests if needed.
- **Monitoring**: As mentioned, logging queries and usage metrics is important. Also track costs (each answer costs tokens). If deployed widely, you might want to monitor how many API calls are being made, and optimize or put quotas.
- **Improving Knowledge Base**: For sales-related queries, one might integrate internal data (like product info, pricing, documentation) rather than relying purely on web search. That leads to the advanced extension of connecting a vector database, which we'll discuss next.

Finally, always ensure that any sensitive data remains secure:

- The .env should not be exposed, and when deploying, set env variables in the hosting environment.
- If connecting to internal databases, use secure connections and do not expose raw data to the user, only through the LLM with proper filtering.

With good error handling, some caching, and mindful use of resources, our agent should run smoothly. Now, let's explore how we can extend this agent further for more advanced use cases, such as using embeddings or deploying as a service.

---

# Advanced Use Cases and Extensions

Our SalesAgent is currently built to search the web and answer questions. However, many real-world scenarios might require additional capabilities. In this section, we'll outline some advanced extensions and how you might integrate them:

## Enhancing Retrieval with Embeddings

While keyword-based search via Tavily is powerful for web data, sometimes we have domain-specific documents (e.g., sales manuals, product sheets, client FAQs) that we want to use for answering questions. These might not be accessible via a web search, or we might want faster lookup. This is where **embeddings** come into play.

**Embeddings** convert text into high-dimensional vectors such that semantically similar texts have closer vectors. By using embeddings, we can do semantic search in a vector database (also known as a vector store). This approach can complement or even replace a live web search for certain use cases.

For example, we could maintain an internal knowledge base:

- A set of documents (PDFs, markdown files, etc.) that contain sales-related information.
- We can use an embedding model (like OpenAI's text-embedding-ada-002 or other open-source models) to encode all these documents into vectors and store them in a database.
- When a user asks a question, we embed the query and find the most similar document chunks via cosine similarity.
- The retrieved chunks then act as context for the answer generation, similar to how Tavily results did.

This technique is used in many QA systems. LangChain provides a framework for this with **Retrievers** and **VectorStores** (Pinecone, FAISS, etc.). Even Tavily has a "Hybrid RAG" mode where it can search both web and a provided database ([Python - Tavily Docs](https://docs.tavily.com/sdk/reference/python#:~:text=Python%20,and%20an%20existing%20database%20collection)) ([Boost Your RAG Performance with Tavily Search API | by Minh Le Duc](https://medium.com/@minhle_0210/boost-your-rag-performance-with-tavily-search-api-607a6437ab8e#:~:text=Boost%20Your%20RAG%20Performance%20with,rapid%2C%20and%20permanent%20search%20results)).

To integrate embeddings into our agent:

- We could add another node in our LangGraph after or parallel to Tavily search, which searches an internal vector store.
- For instance, Node "embeddings_search" that takes the query, searches the vector DB, returns some relevant text segments.
- Then our state could have `internal_results` in addition to `search_results`.
- We could then combine the context from web and internal sources for validation and answering.

Alternatively, we might do something like:

- Try answering from internal data first; if not sufficient, then do a web search.
- Or vice versa.

**Example integration**:
Suppose we have a vector store (using FAISS for local simplicity):

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Assuming 'documents' is a list of strings or LangChain Documents
embedding_model = OpenAIEmbeddings()  # uses OpenAI's embedding endpoint
vectorstore = FAISS.from_texts(documents, embedding_model)
```

At query time:

```python
query_embedding = embedding_model.embed_query(user_query)
docs_and_scores = vectorstore.similarity_search_with_score(user_query, k=3)
```

This gives top 3 relevant docs with similarity scores.

We can then format those docs similarly and include in context.

LangChain also has higher-level `RetrievalQA` chains that handle this, but using it within our graph might complicate our custom logic. Instead, treat it as another tool.

In summary, adding embeddings would greatly enhance the agent’s ability to handle company-specific or niche questions where web search isn't enough. It requires maintaining an up-to-date vector index of your knowledge base. The payoff is quick semantic matches that an LLM can use directly.

## Connecting with Vector Databases

As mentioned, vector databases (like Pinecone, Weaviate, Chroma, etc.) are commonly used to store embeddings for large-scale retrieval. If our sales documents are numerous or updated frequently, a vector DB is useful.

To use one:

- Decide on a vector DB service (e.g., Pinecone for managed service).
- Use their client libraries to index documents (LangChain can help with its VectorStore wrappers).
- In our agent, instead of (or in addition to) Tavily, query the vector DB for relevant passages.

You might then either:

- Combine results: e.g., take the top 5 Tavily results and top 5 internal docs, and feed all to the LLM in context (maybe too much, so perhaps top 3 of each).
- Or prioritize one over the other depending on query type: maybe detect if the query is about internal info vs general knowledge.

This could be an advanced conditional: e.g., a node that classifies query type (LLM can do this too: "Is this asking about our company info or general knowledge?"). Based on that, route to internal search or web search. LangGraph could handle that with a conditional edge branching to different search strategies.

**Implementing hybrid retrieval** (briefly):

- Node: `classify_query` (LLM prompt: output "internal" or "web" category).
- If "internal", go to `node_internal_search` that queries vector DB.
- If "web", go to `node_search` (Tavily).
- Possibly if "both", do both and merge.

Though this adds complexity, it shows how extendable the graph approach is. You can always add more nodes and logic for advanced flows.

## Deploying as a Web Service

So far, we built a Streamlit app which is great for user interaction in a browser. But sometimes you want the agent behind an API or integrated into another application (say a chat widget on a website, or a Slack bot, etc.). In those cases, deploying as a web service (without the Streamlit UI) might be more appropriate.

To do this:

- You could use a framework like **FastAPI** or **Flask** to create an HTTP endpoint that accepts a question and returns an answer (and maybe the sources).
- Inside the endpoint, you would call the same workflow logic (the graph). Since our LangGraph and supporting code is modular, you can reuse `compiled_graph.invoke` in any context.

Example with FastAPI:

```python
from fastapi import FastAPI
app = FastAPI()

@app.post("/ask")
async def ask_question(query: str):
    initial_state = {
        "user_query": query,
        "search_results": [],
        "needs_search": True,
        "refine_query": None,
        "final_answer": None
    }
    result_state = compiled_graph.invoke(initial_state)
    answer = result_state.get("final_answer", "I'm sorry, I don't have that information.")
    return {"question": query, "answer": answer}
```

You would run this with an ASGI server (like Uvicorn) and now any client (web app, mobile app, chatbot, etc.) can hit the `/ask` endpoint with a query to get a JSON response. This decouples the frontend from the backend; you could then build a custom UI or integrate into existing systems.

**Scaling the web service**:

- If using FastAPI, you can run multiple workers (with Uvicorn or Gunicorn) to handle concurrent requests.
- Ensure thread safety or use async calls for IO-bound operations (OpenAI's Python SDK and Tavily might have async methods).
- Use a load balancer if needed for heavy load.
- Containerize the app with Docker for deployment convenience.

**Security**:

- If deploying an API, consider authentication (you might not want it publicly open if it's internal).
- Rate limit the API to prevent abuse or accidental overload (especially since each call costs token$).
- Hide API keys (never expose them in client-side code; in FastAPI the keys stay on server side).

**Monitoring and Maintenance**:

- Add monitoring for uptime and performance (like how many seconds each request takes, so you know if it gets slow).
- Monitor costs if this runs a lot.
- Keep logs of queries (if allowed by privacy) to identify common questions and maybe add those to a FAQ or tune the system.

In a company setting, one might deploy this agent as a Slack bot using Slack API, where each message from a user triggers the agent and the bot posts the answer. Or as part of a CRM system for sales reps to quickly query info.

The flexibility of our design (modular nodes and state) means we can adapt it beyond just a Streamlit app.

---

# Final Project: End-to-End Implementation

Congratulations on making it this far! In this final section, we'll put everything together and walk through the entire code and usage of the SalesAgent system. This will serve as a recap and a final reference implementation.

## Code Walkthrough

Let's assemble the core components into one coherent code listing. We will assume that the necessary API keys are set in the environment and that you installed all required libraries.

```python
# sales_agent.py

import os
import json
from typing import List, Optional, Any, TypedDict

from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables (TAVILY_API_KEY, OPENAI_API_KEY, etc.)
load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not TAVILY_API_KEY or not OPENAI_API_KEY:
    raise RuntimeError("API keys not set in environment. Please set TAVILY_API_KEY and OPENAI_API_KEY.")

# Initialize API clients
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
# OpenAI API key is picked up from environment by LangChain automatically if set.

# Define the GraphState using TypedDict
class GraphState(TypedDict):
    user_query: str
    search_results: List[Any]
    needs_search: bool
    refine_query: Optional[str]
    final_answer: Optional[str]

# Helper: format search results for prompt
def format_results_for_prompt(results: List[Any]) -> str:
    if not results:
        return "No results."
    formatted_list = []
    for idx, res in enumerate(results, start=1):
        title = res.get("title", "")
        content = res.get("content", "")
        snippet = content
        if len(snippet) > 200:
            snippet = snippet[:200] + "..."
        formatted_list.append(f"[{idx}] {title}: {snippet}")
    return "\n".join(formatted_list)

# Initialize the language model (ChatGPT)
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

# Prompt templates for validation and answering
validation_prompt = PromptTemplate(
    input_variables=["question", "results"],
    template=(
        "You are an assistant tasked with deciding if the provided information is enough to answer a question.\n"
        "Question: {question}\n"
        "Information:\n{results}\n\n"
        "If this information is sufficient to answer the question, output JSON: {\"need_search\": false}.\n"
        "If more information is needed, output JSON: {\"need_search\": true, \"refine_query\": \"<a better search query>\"}.\n"
        "Respond only with JSON."
    )
)

answer_prompt = PromptTemplate(
    input_variables=["question", "context"],
    template=(
        "You are an assistant answering the user's question using the given context.\n"
        "Question: {question}\n"
        "Context:\n{context}\n\n"
        "Answer the question based on the context. If the context is insufficient, say \"I'm sorry, I don't have that information.\""
    )
)

# Define node functions:
def node_search(state: GraphState) -> GraphState:
    query = state["user_query"]
    if state.get("refine_query"):
        query = state["refine_query"]
    logger.info(f"Searching for: {query}")
    try:
        response = tavily_client.search(query, max_results=5, search_depth="advanced", include_raw_content=False)
        results = response.get("results", [])
    except Exception as e:
        logger.error(f"Tavily search error: {e}")
        results = []
    state["search_results"] = results
    # Reset refine_query to avoid reusing it unless set again
    state["refine_query"] = None
    return state

def node_validate(state: GraphState) -> GraphState:
    question = state["user_query"]
    results_text = format_results_for_prompt(state.get("search_results", []))
    prompt_text = validation_prompt.format(question=question, results=results_text)
    logger.info("Validating if more search is needed...")
    try:
        raw_response = llm.predict(prompt_text)
    except Exception as e:
        logger.error(f"Validation LLM error: {e}")
        # If error, assume we have to proceed with current info
        state["needs_search"] = False
        state["refine_query"] = None
        return state
    raw_response = raw_response.strip()
    # Extract JSON part if the model gave extra text
    if raw_response and raw_response[0] != "{":
        start = raw_response.find('{')
        end = raw_response.rfind('}')
        if start != -1 and end != -1:
            raw_response = raw_response[start:end+1]
    try:
        decision = json.loads(raw_response)
    except json.JSONDecodeError:
        logger.warning(f"Failed to parse JSON from LLM: {raw_response}")
        # Default to no further search to avoid loop
        state["needs_search"] = False
        state["refine_query"] = None
        return state
    need_search = decision.get("need_search", False)
    refine_query = decision.get("refine_query")
    state["needs_search"] = need_search
    state["refine_query"] = refine_query if need_search else None
    logger.info(f"Validation result -> need_search: {need_search}, refine_query: {refine_query}")
    return state

def node_answer(state: GraphState) -> GraphState:
    question = state["user_query"]
    results = state.get("search_results", [])
    # Build context from results
    if not results:
        state["final_answer"] = "I'm sorry, I don't have that information."
        return state
    # Use up to top 3 results' content
    context_snippets = []
    for res in results[:3]:
        content = res.get("content") or res.get("raw_content") or ""
        if content:
            # Limit each snippet length to avoid overflow
            if len(content) > 1000:
                content = content[:1000] + "..."
            context_snippets.append(content.strip())
    context = "\n\n".join(context_snippets)
    prompt_text = answer_prompt.format(question=question, context=context)
    logger.info("Generating final answer...")
    try:
        answer = llm.predict(prompt_text).strip()
    except Exception as e:
        logger.error(f"Answer LLM error: {e}")
        state["final_answer"] = "I'm sorry, I couldn't generate an answer."
        return state
    state["final_answer"] = answer
    logger.info(f"Final answer generated.")
    return state

# Build the LangGraph workflow
from langgraph.graph import StateGraph, START, END
graph = StateGraph(GraphState)
graph.add_node("search", node_search)
graph.add_node("validate", node_validate)
graph.add_node("answer", node_answer)
graph.add_edge("search", "validate")
# Conditional edge: from validate, decide next
def route_after_validate(state: GraphState) -> str:
    return "search" if state.get("needs_search") else "answer"
graph.add_conditional_edges("validate", route_after_validate, {"search": "search", "answer": "answer"})
graph.add_edge("answer", END)
graph.set_entry_point("search")
compiled_graph = graph.compile()

# The compiled_graph is now ready to run with an initial state
```

Let's review what we have:

- We set up logging and loaded API keys.
- Defined GraphState and helper functions.
- Created prompt templates for validation and answer.
- Wrote node functions for search, validate, answer with logging at each step.
- Built the graph (nodes + edges + conditional routing).
- Compiled the graph.

This `sales_agent.py` script can be run to initialize everything. The `compiled_graph` object is what we use to process queries.

We can test this with a simple input (outside of Streamlit for now, say in a Python shell or as a quick test):

```python
if __name__ == "__main__":
    test_query = "Who is Lionel Messi?"
    initial_state = {
        "user_query": test_query,
        "search_results": [],
        "needs_search": True,
        "refine_query": None,
        "final_answer": None
    }
    result = compiled_graph.invoke(initial_state)
    print("Question:", test_query)
    print("Answer:", result.get("final_answer"))
```

If all goes well, it should print an answer about Lionel Messi (likely summarizing who he is, since the info will be from Britannica or Wikipedia).

We could integrate this with the Streamlit UI we described earlier, but for brevity, let's ensure the focus is on the workflow code.

## Deploying the System

With the code in place, deploying can mean either:

- Running the Streamlit app:
  - Save the Streamlit part (the code snippet we wrote in the Streamlit section) in a file, say `app.py`, that imports everything from `sales_agent.py`. For example:
    ```python
    from sales_agent import compiled_graph
    # (plus streamlit code for UI)
    ```
  - Then run `streamlit run app.py`. This will open a local web server where you can interact with the agent. Deploy that to a server or Streamlit cloud for others to access.
- Running as an API service:
  - Use the FastAPI snippet; similarly import `compiled_graph` and run a uvicorn server. Then integrate with whatever frontends or tools via HTTP calls.

In a corporate environment, one might containerize the app:

- Create a Dockerfile including all dependencies and environment variables (but ensure not to bake API keys into the image; supply them at runtime).
- Then run the container on a cloud service or Kubernetes.

Make sure to set appropriate environment variables for keys on the server.

## Debugging and Troubleshooting

If you encounter issues, here are some tips:

- **Node functions not executing as expected**: Ensure the node names in edges match exactly the names added (typos can cause a node to be a "dead end"). The LangGraph compile might warn if something is unreachable. Our use of `set_entry_point` and adding edges should cover it. If the graph doesn't run, use the Mermaid visualization technique to inspect the graph structure.
- **LangGraph state issues**: If a node returns a state missing some required keys, it might cause errors in subsequent nodes. Our GraphState keys cover all we use and we maintain them. If you add new state variables, ensure to carry them through properly.
- **Tavily API issues**: If you get no results often, test queries directly on Tavily or ensure your API key is valid. Maybe use `include_answer="advanced"` for more thorough answers, although we didn't use `include_answer` to let our LLM handle it.
- **OpenAI API errors**: If you hit rate limits (error 429) or other errors, you might need to throttle calls or use a paid account with higher limits. Our app does sequential calls, so normally not too many in parallel, but a burst of users could hit limits. The log will show if an API call failed.
- **JSON parsing issues**: If the validation LLM outputs not exactly JSON (especially if using a model that sometimes adds text), check the log of `raw_response`. Tweak the prompt if necessary (e.g., emphasize "ONLY JSON" or use the `StructuredOutputParser` approach which might yield more consistent results). For GPT-4 this is usually reliable; for GPT-3.5, you might occasionally get something like `"need_search": false\nThe information is enough.` which our code would trim to JSON correctly (due to braces handling).
- **Loop never ends**: If you find the agent looping (maybe printing "Searching..." multiple times) without concluding, likely the validation is stuck returning true. Check what refine_query it suggests and what results come. Possibly it's not finding what it needs and not giving up. In that case, implement the iteration cap as discussed. For example, add `state["iteration"]` and in router, if `iteration >= 3` then go to answer regardless. Or adjust the validation prompt to be more willing to stop (like if it already refined once).
- **Answer quality issues**: If the answers are incorrect or not using the context properly, consider:
  - Check if the context actually contained the info. Maybe Tavily results weren't great. In that case, maybe refine queries manually and see. Possibly the validation didn't catch that info was insufficient. This may require prompt tuning or adding some cross-check.
  - Try increasing number of results or including raw_content for important results.
  - If answers are too verbose or too brief, adjust the prompt instructions (e.g., "Answer in 2-3 sentences" or remove "concise" if it's cutting short).
  - Use GPT-4 for better reliability if not already.
- **Streamlit gotchas**: If you make changes to the code, Streamlit sometimes needs a full rerun (there is a "Rerun" button or just refresh the browser). If you add new environment variables, you might need to restart the app.

By testing a variety of questions (simple ones, ones requiring multiple hops, ones with no answer), you can refine the prompts and logic. This iterative development is normal in LLM applications.

At this point, you should have a fully functional SalesAgent that demonstrates:

- Custom workflow control with LangGraph (including loops and conditional logic).
- Integration of a search tool (Tavily) for real-time information.
- Solid prompt engineering for decision making and answering with LangChain.
- A user-friendly interface via Streamlit.

This project showcases how advanced developers can orchestrate multiple components to build a complex AI system. The modular nature means you can extend or modify parts to suit new requirements (e.g., different tools, more nodes, alternate prompts). We encourage you to experiment further: maybe add memory for follow-up questions to make it conversational, or allow the user to give feedback if the answer was good or not to further tune the system.

Good luck, and happy coding!
