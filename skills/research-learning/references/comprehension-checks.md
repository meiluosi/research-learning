# Comprehension checks

Every lesson ends with two questions. They check understanding and push toward research.

## The two questions

1. **A principle question.** Why is the design as it is? Aim at one design choice and ask for the reason, in the learner's own words. Example: "Why does the score get divided by sqrt(d), and not by d?"
2. **A research question.** What would happen if a part were changed, and how would you tell? It should have no known single answer in the lesson, and should be testable. Example: "If you replaced softmax with a sigmoid, what would change in the training behavior, and what would you measure?"

Give a hint about where to look for the second one (stability, scale, cost), not the answer.

## Responding to the learner's answer

When the learner answers, start the next lesson with a response:

1. **What is right**, stated specifically ("You are right that the scale cannot be controlled just by adding a parameter").
2. **What to fix**, precisely and with numbers if possible. Do not blur an error into praise.
3. **The reason**, with a small example.
4. **How it connects** to the next step.

Never call a wrong answer partly right just to be encouraging. If it is half right, say which half.

## Predict first

Before showing a result or running an experiment, ask the learner to write a prediction: "What do you expect to happen, and why?" Then show the result. A wrong prediction is the most useful thing in the lesson; say so.

## Keep it light

Two questions, not five. If the learner has not asked for more, do not quiz them.
