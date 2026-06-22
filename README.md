# Skills Testing

## Research Question
How can we benchmark the effectivenes of Skills?

## Definitions

* Skills
    * A self-contained unit of capability: a combination of instructions (typically in a SKILL.md file), scripts, and resources that an AI agent can discover and execute to perform a specific task.
    > Think of it as a modular plugin for an AI agent's toolbox.

## Resources

* [Agent Eval Harness](https://github.com/opendatahub-io/agent-eval-harness)
    * Generic evaluation framework for agents and skills. Analyze, run, score, and improve skills automatically across different agent harness (Claude Code, OpenCode, Agent SDK).
    * The primary objective of an agent evaluation harness like this one is to measure the performance, reliability, and cost-efficiency of AI agents focusing on their Skills.
    * [My notes on the project](https://github.com/wbenchesser/agent-eval-harness-testing)
* [Cloudflare Vulnerability Scanning: Skills](https://blog.cloudflare.com/build-your-own-vulnerability-harness/#it-all-starts-with-a-skill)
    * "The real value lives in the prompts themselves, and our prompts continue to carry the initial skill's attacker scenarios, bug classes, and anti-pattern detections nearly unchanged."
    * Supports the use of more agents. Agents with different roles doing precise, individualized tasks have good results. 
    * This team used:
        * Three "researchers"
            * Do recon and write an architecture.md
        * One "hunter" per attack class 
            * Trying to break the code rather than review it.
        * Adversarial Validators
            * Attempt to disprove each finding. 
            * survivors are written up as a human-readable vulnerability report.
        * A fresh agent independently re-verifies every finding against the source.
    * One of the big takeaways is that when looking at the coverage metrics, a single run finds only about half the bugs you'd catch across multiple runs. The ones that are found tend to be skewed toward the simpler and less subtle.
        