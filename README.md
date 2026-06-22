# Skills Testing

## Research Question
How can we benchmark the effectivenes of Skills?

## Definitions

* Skills
    * A self-contained unit of capability: a combination of instructions (typically in a SKILL.md file), scripts, and resources that an AI agent can discover and execute to perform a specific task.
    > Think of it as a modular plugin for an AI agent's toolbox.
* Harness
    * Execution Harness
        * Also known as an agent harness or agent runtime, this is the code that turns a static language model into an active, decision-making agent. It manages the state machine and the loop of interaction.
    * Evaluation Harness
        * This is a specific framework. It sits entirely separate from the live agent system to test its capabilities.

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
        
## Benchmarking
* What does it mean to benchmark a skill? Unlike standard prompt engineering, you are testing two distinct capabilities:
    1. **Intent Recognition**: did the agent trigger the skill at the right time?
    2. **Procedural Execution**: did the agent execute the workflow consistently and efficiently?

### Possible Metrics
1. **Trigger Accuracy (Activation Rate)**: 
    * Since Claude uses progressive disclosure (reading the YAML frontmatter to determine if a skill is relevant), you must measure how reliably it triggers.  
    * Target: >90% activation on relevant queries; 0% activation on completely unrelated queries (false positives).
2. E**xecution Consistency (Determinism)**: 
    * One of the primary goals of a skill is repeatability. If you pass the same input multiple  times, does the layout, tone, and file structure remain uniform?  
3. **Orchestration Efficiency**: 
    * If your skill coordinates with the [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro) (MCP) or external tools, track the number of tool calls. A high-performing skill drops the number of exploratory actions or errors an agent makes.
4. **User Correction Rate**: 
    * How often does a human have to intervene with statements like "No, follow step 3" or "You forgot the style guide"? 
    * A successful skill drops human course-correction to near zero.