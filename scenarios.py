"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        "texts": [
            "I keep a short list beside my keyboard because small decisions disappear quickly. When I finish a task, I write down what changed and why, even if the answer seems obvious at the time.",
            "The hallway light flickered twice before breakfast. I replaced the bulb after lunch, but I left the old one on the counter because I wanted to remember that the problem had been simple.",
            "I prefer tests that explain what went wrong. A green check is useful, but a failure that names the input and the expected result teaches me where my assumption was wrong.",
            "On busy mornings I make coffee before I open my messages. It is not a productivity system, just a small pause that keeps the first urgent request from choosing the shape of the whole day.",
            "The first draft of this note was too tidy. I put back the awkward sentence because it described the decision more honestly than the polished version did.",
            "I learned the route by missing the turn three times. Now I notice the blue sign early, though I still slow down there because habit is not the same thing as attention.",
            "A useful tool should make the next step clearer, not hide the work behind a confident button. When I cannot explain what a button did, I do not trust the result yet.",
            "Our meeting ended with fewer decisions than expected. That was fine. We separated the questions we could answer today from the ones that needed someone else to look at the evidence.",
            "I save examples of mistakes because memory edits them into cleaner stories. The screenshot with the wrong filename is more useful than the final folder when I am trying to understand the sequence.",
            "There is a difference between being finished and being ready to show someone else. I check the edge cases after the main path works, then I write down the one limitation I still would not want to hide.",
        ],
    },
    {
        "name": "label coverage",
        "criterion": 2,
        "texts": [
            "In conclusion, this comprehensive analysis demonstrates that the implementation of a robust and scalable solution provides significant value across a wide range of operational contexts. The following sections summarize the key findings and recommended next steps.",
            "I missed the bus, bought a warm cheese roll, and arrived ten minutes late. The driver shrugged when I apologized, which somehow made the whole morning feel less serious.",
            "The plan is reasonable, but the evidence is thin. I would keep the change behind a flag for one week, compare the error reports, and decide after seeing which cases actually move.",
        ],
    },
    {
        "name": "malformed input safety",
        "criterion": 3,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": "x", "creator_id": "eval_bad_short"},
            {"text": ["not", "text"], "creator_id": "eval_bad_list"},
        ],
    },
    {
        "name": "complete decision response",
        "criterion": 4,
        "texts": [
            "A decision should carry enough information to be checked later. The identifier, both signals, the combined confidence, the short guess, and the reader-facing label all belong together.",
            "I changed one setting and wrote down the old value first. That small habit makes a rollback less dramatic because the previous state is not something I have to reconstruct from memory.",
            "The report is useful only when its numbers still point to the request that produced them. I would rather have a plain identifier than a beautiful summary that cannot be traced.",
            "A rejection is also a result. If the service refuses a request, the reason and the caller should remain visible instead of disappearing between the client and the server.",
            "The final check is not a ceremony. I read the response as if I were debugging it tomorrow, when the terminal is closed and the original intention is no longer obvious.",
        ],
    },
    {
        "name": "repeatable scores",
        "criterion": 5,
        "texts": [
            "A stable detector should give the same input the same score when its configuration and model remain unchanged. Repeating a measurement helps separate a real behavior from a lucky observation.",
            "The window was open during the storm, so the papers moved across the desk. I closed it, gathered the pages, and put the unfinished note back where I could find it.",
            "A threshold is a decision rule, not a fact about authorship. It should be explained in terms of the signals and checked against examples that make its weak spots visible.",
            "I do not want a log that merely says success. I want the request identity, the inputs used for the decision, and the outcome that a later reader can compare with the original evidence.",
            "When a repair changes behavior, I rerun the old examples before I trust the new result. The point is not to preserve every number, but to know which change caused the difference.",
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
