# Write-Up

## 1. Why I chose these questions

I picked questions about friction, exchange, and frame because they are close to how people actually replay a day in their head. Most people do not naturally think, "What is my locus of control score?" They remember a moment where plans shifted, whether they spent the day giving or waiting, and whether the story stayed inside their own stress or widened to other people. I wanted prompts that sounded like a calm colleague helping someone notice patterns already present in memory.

I also chose moments that can hold tension without turning into confession. "What kept your attention on the outside pressure?" and "What felt most absent or overdue?" allow someone to name frustration without being told they are wrong for having it. That mattered to me because the assignment is not to sort people into good and bad categories; it is to help them see the shape of a day.

## 2. How I designed the branching

I kept the tree binary at the decision level even though each question has four options. That was a deliberate trade-off. Four-way branching at every step would make the tree feel expansive, but it would also make the overall conversation harder to follow and harder to summarize. Instead, I used four fixed choices to give the user a more natural way to answer, then grouped those options into two underlying directions per axis.

I also made each axis feel like a mini-arc: a routing question, a branch-specific follow-up, then a reflection and bridge. That gave me enough room to personalize the conversation without letting the three axes feel like separate quizzes glued together. The bridges matter more than they look; they are what make the flow feel continuous.

## 3. Sources and how they shaped the tree

Rotter's locus of control and Dweck's growth mindset informed Axis 1. Instead of asking whether someone was "being accountable," I asked what line sounded like them when the day pushed back, then followed with either visible agency or visible pressure. That keeps the theory grounded in how people interpret setbacks.

Campbell's work on entitlement and Organ's work on organizational citizenship behavior informed Axis 2. I translated that into the difference between remembering the day as giving versus remembering it as not receiving enough. The contribution branch asks for concrete forms of added value; the entitlement branch asks what felt absent or overdue, because entitlement often shows up as attention to missing reciprocity.

Maslow's self-transcendence and Batson's perspective-taking informed Axis 3. I wanted the distinction to be about radius, not virtue. That is why the self branch asks what the narrow frame was protecting, while the other branch asks who became present in the wider frame.

## 4. What I would improve with more time

With more time, I would make the summary language slightly more adaptive so it could refer to the dominant pattern in more natural prose than the raw labels "internal," "entitlement," or "other." I would also add a lightweight authoring validator for unreachable nodes and maybe a small test harness around the CLI.

The main thing that still feels incomplete is depth inside each branch. Right now the tree is coherent and deterministic, but it is still a relatively compact conversation. A longer version could add one more invisible decision inside each branch to produce even more specific reflections while preserving the same three-axis structure.
