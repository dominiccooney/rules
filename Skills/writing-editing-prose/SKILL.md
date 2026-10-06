---
name: writing-editing-prose
description: Draft or revise any English text, including PR descriptions, significant comments, extended messages to the user, documentation, etc.
---

# Writing and Editing Prose

We write so that the reader understands what we want and does it. Simple, direct writing serves that purpose. Writing that tries to sound clever or wise gets in the reader's way. Our readers live all over the world and many read English as a second language. Be exact about details and kind to people.

Write in four steps: organize, write, revise, edit. Each step below has its own checks. Revise and edit after the draft exists, as separate passes; a draft written with care still contains the faults these passes look for.

## Tone

When writing for others: Affect a wilful, dynamic, welcoming, inclusive, pro-people, humble, inquisitive tone. Avoid closed-ended questions.

When writing for me, you can be as direct as you like. I am an Australian and I'm comfortable with very direct communication.

## Audience

This my rules and skills' concepts — the levels, placement, the matrix, storage contracts, invariants, consistency boundaries — are a working vocabulary between you and me. Use it freely in plans, in development discussion, and in your own notes. Other readers, (someone reading code we wrote; the author of code you review; etc.) does not share that vocabulary. Give them the finding in the words of the code and the product: name the two things that meet and what goes wrong where they meet. Write "a session started in the desktop app and deleted from the CLI leaves its worktree behind," not "the CLI cell of the worktree row is missing." Write "users who rely on the foreground terminal lose it, and nothing in the PR says they were asked," not "this fails the need check." Use terms from the code and the product. Do not use terms from this document.

When writing for external contributors, consider adding a small "plus alpha" of thanks and friendly encouragement. These people are not employees and took time to engage with us and we should thank them for that. If we can't act on their direct suggestions we are still grateful for their time and input and consider adding a phrase that indicates we're open to future contributions from them. (We usually DON'T need such language for our teammates who will appreciate brevity more.)

## Organize: The Pyramid Principle

In written communication beyond a few sentences, for example bug reports, PR descriptions, and module comments, use the Pyramid Principle to communicate clearly.

Here is a step-by-step guide to applying the Pyramid Principle:

1. What SUBJECT are you discussing?
2. What QUESTION are you answering in the reader's mind?
3. What is the ANSWER?
4. What is the SITUATION? Make the first non-controversial statement you can about what is going on.
5. What is the COMPLICATION? Ask yourself, "so what?" Think of something in the SITUATION to raise the QUESTION.
6. Do the QUESTION and ANSWER still follow? If not, change the QUESTION to the one raised by the COMPLICATION, or use a different COMPLICATION.

Start to compose an introduction. You can vary the order to change the tone:

CONSIDERED: Situation, Complication, Solution
DIRECT: Solution, Situation, Complication
CONCERNED: Complication, Situation, Solution

7. What NEW QUESTION is raised by the ANSWER? Then, the KEY LINE not only answers this question but gives the plan of the PR description. Decide whether you will answer INDUCTIVELY or DEDUCTIVELY.

If the group is inductive, it must either deal with cause and effect and should be ordered by time; or divide a whole into its parts and be ordered by structure; or classify like things and be
ordered by rank.

Time order: Ask yourself, "What would I do first if I were doing this? What second? etc."

Structural: Are the pieces mutually exclusive and collectively exhaustive (MECE) in terms of the whole? How do you order the pieces? To reflect a process, use time order; to emphasize location, use structural order (for example, geography); otherwise rank them (by whatever is relevant--size, priority, etc.)

Ranking: What do you label the points as? (What is the "group noun"?) Can you find anything more specifically the same about them? Can you justify their order on that basis? Are there any missing?

When using the Pyramid Principle, do NOT use "Situation", "Complication", etc. as headings. These are conceptual labels for you, but the structure should be invisible and self-supporting to the reader so that they can focus on the content and meaning of your writing.

## Write

Write the draft plainly. Say what the thing is, what is wrong with it, and what to do. Concrete nouns and verbs carry the meaning; adjectives and adverbs rarely add any.

Every sentence mixes *given* information, which the reader already has from earlier sentences or from context, with *new* information, which the sentence introduces. Readers understand a sentence by attaching the new information to the given. So put given information first and new information last. The same rule orders a paragraph: each sentence begins from what the sentence before it left the reader holding.

A counter-example, with new information first and given information last:

> Carefully consider word order. In a sentence, introduce new concepts later; put familiar words earlier. Flowing writing is created by ordering concepts from novel to familiar. Easy-to-comprehend writing is flowing writing.

Prefer the active voice, but use the passive when it puts the given information first.

Use parallel structure for parallel ideas. Above: "put given information first and new information last."

## Revise

Revise the whole draft before editing lines. Read it as the reader, who does not know what you meant. Check:

- Does the first paragraph answer the reader's question? (See the Pyramid Principle.)
- Is every noun phrase present that the reader needs? Compare the draft with what you know. A step you skipped in the text because it was obvious to you is missing for the reader.
- Are the paragraphs in the reader's order, not the order you discovered things in?
- Could the reader act on the draft and do the wrong thing? Find the sentence that permits the wrong reading and fix that sentence.

Revising also catches a fault of your own: in a long reply or on an abstract topic, the draft can turn into fluent prose that says nothing the reader can act on. Test each paragraph by restating it as a plain fact or a plain instruction. Shorten or delete any paragraph that will not restate.

## Edit Line by Line

Edit the draft line by line, after revising. The faults below are listed with the ones that cost the reader most first; check for them in that order.

**Missed connections.** Every *this*, *that*, *it*, *one*, *these*, *which* and *such* must have one obvious noun as its referent, in the same sentence or the one before. If a reader could attach the pronoun to two nouns, repeat the noun. If the referent is a whole clause or idea, name it: "this gap," "that check," not "this." The same test applies to *the former*, *the latter*, *respectively* and to any noun phrase that assumes an earlier definition.

**Slogans and antitheses.** A balanced pair ("X, not Y"; "a question, not an answer") and a sentence that could be quoted as a maxim both state a conclusion without the fact or instruction behind it. Rewrite each as a plain statement of what is so and what to do. The plain version is often longer. Keep it anyway.

**Figures of speech.** Delete clichés. Do not invent metaphors. A term defined in this document (for example *reach*) may be used because the reader can look up the definition. When a comparison helps, compare with a common object that every reader knows, and state the plain meaning beside it.

**Consistent language.** One word for one concept. A second word for the same concept implies a distinction the reader will look for and not find.

**Simple language.** Choose the short, common word. Words of Anglo-Saxon origin are usually shorter, plainer and known to more readers than their Latin or French equivalents: "teammate" over "colleague," "start" over "initiate," "use" over "utilize." When two words compete, look at where each came from and what it once meant. Ut multitudini variae placeas, noli lingua Latina uti.

**Unnecessary words.** Cut them. Then cut the sentence that repeated the sentence before it. A short text that says everything the reader needs is complete; do not add to it. Each revision of a text should leave it the same length or shorter. PR descriptions break this rule most often: each update adds a paragraph and removes none. When you update a description, delete or replace text before you add any.

**Verbs.** Prefer the active voice and a finite verb over a gerund or a nominalization ("we decided," not "the decision was made"; "delete," not "deletion of"). Keep the passive where it puts given information first.

**Sentence length.** Vary it. A run of short sentences reads as a list of slogans; a run of long ones tires the reader.

**Closing formulas.** Delete stock closings ("Say the word and I'll…", "Let me know if…"). End when the content ends.

## Typesetting

Wrap git commit messages at 76 characters.

GitHub PRs and issue text will be wrapped by the user agent. Don't add carriage returns within paragraphs.
