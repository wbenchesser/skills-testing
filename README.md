# Skills Testing

## Research Questions
1. How can we benchmark the effectivenes of Skills?
2. If we plan to use security skills to meet security goals in the Agentic Development Life Cycle (ADLC), how reliable are they?

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
* [The ProdSec Skills Reposoitory](https://github.com/RedHatProductSecurity/prodsec-skills)
    * Security skills for AI coding assistants and agentic systems. Skills encode security recommendations, guidelines, and best practices.
        
## Benchmarking
* What does it mean to benchmark a skill? Unlike standard prompt engineering, you are testing two distinct capabilities:
    1. **Intent Recognition**: did the agent trigger the skill at the right time?
    2. **Procedural Execution**: did the agent execute the workflow consistently and efficiently?

### Possible Metrics
1. **Trigger Accuracy (Activation Rate)**: 
    * Since agents use progressive disclosure (reading the YAML frontmatter to determine if a skill is relevant), you must measure how reliably it triggers.  
    * Target: >90% activation on relevant queries; 0% activation on completely unrelated queries (false positives).
2. E**xecution Consistency (Determinism)**: 
    * One of the primary goals of a skill is repeatability. If you pass the same input multiple  times, does the layout, tone, and file structure remain uniform?  
3. **Orchestration Efficiency**: 
    * If a skill coordinates with the [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro) (MCP) or external tools, track the number of tool calls. A high-performing skill drops the number of exploratory actions or errors an agent makes.
4. **User Correction Rate**: 
    * How often does a human have to intervene with statements like "No, follow step 3" or "You forgot the style guide"? 
    * A successful skill drops human course-correction to near zero.

## Approach

Any project wishing to address the research questions will need to focus on measuring the effectiveness of skills both in isolation and when used at scale in the ADLC. The approach should consist of the following key components:

1. **Isolated Skill Testing**: Evaluate individual skills in controlled environments to establish baseline performance metrics for trigger accuracy, execution consistency, orchestration efficiency, and user correction rates.

2. **ADLC Integration Testing**: Deploy skills within the full ADLC workflow to measure their effectiveness in realistic development scenarios, including how they interact with other skills and tools.

3. **Vulnerability-Based Benchmarking**: Explore the feasibility of benchmarking skill effectiveness against a curated set of known vulnerabilities. This will involve:
   * Drawing from established sources like the OWASP security benchmark and other vulnerability databases
   * Identifying existing projects with documented security issues
   * Creating test scenarios where security skills should detect and address these known vulnerabilities
   * Measuring detection rates, false positives, and remediation quality

4. **Comparative Analysis**: Assess the reliability and accuracy of security skills by comparing their performance against known vulnerability baselines, establishing confidence intervals for their use in production security workflows.

## Example Skills

In order to benchmark effectiveness, we'll want relevant code snippets that we as developers know should be handled by certain skills. Here are some matchups I've found:

1. ProdSec's input-validation-injection
    * Applied when reviewing or writing code that processes untrusted input, constructs queries or commands, or handles user-supplied data. Covers SQL, LDAP, OS command injection, prototype pollution, and general validation strategy.
    > The OWASP benchmark has vulnerability examples relating to SQL Injection, LDAP Injection, Command Injection, and Prototype Pollution. 
2. ProdSec's web-application-security
    * Reviews web application security controls against OWASP-aligned risks. Use when building, auditing, or reviewing server-side web applications that handle user input, sessions, authentication, or access control.
3. ProdSec's differential-review
    * Performs security-focused differential review of code changes (PRs, commits, diffs). Adapts analysis depth to codebase size, uses git history for context, calculates blast radius, checks test coverage, and generates comprehensive markdown reports. Automatically detects and prevents security regressions.
    * Meta-skill that should detect security regressions across categories

## Skills


| ProdSec Skill | Target | Database |
| -------- | -------- | -------- |
| address-sanitizer | Detects memory errors (buffer overflow, use-after-free) | C/C++ apps in OWASP Benchmark |
| admin-interface-security | Secures admin panels and privileged endpoints | The /admin or dashboard routing modules from [OWASP Juice Shop](https://github.com/juice-shop/juice-shop). |
| aflpp | Fuzzes code to discover crash vulnerabilities | Core target suites found in Google's [FuzzBench](https://github.com/google/fuzzbench) repository. |
| agent-identity | Verifies autonomous agent identity | |
| agent-to-agent-auth | Authenticates between agents | |
| agent-to-mcp-server-auth | Secures agent-to-MCP authentication | Transport/authentication test suites inside the [Model Context Protocol (MCP) SDKs](https://github.com/modelcontextprotocol). |
| agentic-actions-auditor | Audits autonomous agent actions |  |
| algorithm-selection | Chooses secure crypto algorithms | Python/Java configuration scripts purposefully selecting weak algorithms (e.g., MD5, DES) vs AES-GCM. |
| apache-camel-security | Secures Apache Camel routes |  |
| atheris | Fuzzes Python code for bugs |  |
| audit-context-building | Builds comprehensive audit context |  |
| authentication | Implements secure authentication |  |
| authentication-enforcement | Enforces auth on all endpoints |  |
| authorization | Validates access control |  |
| avoid-api-keys | Replaces API keys with better auth | Codebases intentionally committed with dummy API keys |
| aws-security | Applies AWS security best practices | [CloudGoat](https://github.com/rhinosecuritylabs/cloudgoat): Rhino Security Labs' "Vulnerable by Design" cloud deployment tool. |
| bidirectional-filtering | Filters input/output data flows | General OWASP benchmark |
| build-yaml-misconfiguration | Detects insecure build configs | [GitHub Actions Goat](https://github.com/step-security/github-actions-goat): Deliberately Vulnerable GitHub Actions CI/CD Environment |
| cargo-fuzz | Fuzzes Rust projects | [Trophy Case](https://github.com/rust-fuzz/trophy-case): A showcase of bugs found via fuzz testing Rust codebases |
| client-metadata-support | Manages OAuth client metadata |  |
| client-side-security | Secures frontend applications | [Simply Vulnerable Application](https://github.com/nleach999/simply_vulnerable_react): React DOM XSS Vulnerabilities |
| codeql | Runs static analysis for vulnerabilities | [Official CodeQL example snippets including vulnerabilities](https://github.com/github/codeql/tree/main/go/ql/examples/snippets) |
| compiler-hardening | Enables security compiler flags |  |
| consent-and-scoping | Manages OAuth consent and scopes | [Ory Hydra OAuth2 Providers Suite](https://github.com/ory/hydra): Mock authorization workflows |
| constant-time-analysis | Detects timing side-channels | [DudeCT Leakage Assessment Engine Examples](https://github.com/oreparaz/dudect/tree/master/examples): includes baseline target binaries (`dudect_donnabad`) displaying severe timing anomalies |
| constant-time-testing | Tests for timing leaks | [DudeCT Leakage Assessment Engine Examples](https://github.com/oreparaz/dudect/tree/master/examples): includes baseline target binaries (`dudect_donnabad`) displaying severe timing anomalies |
| container-hardening | Secures container configurations | [Docker Security: A Practical Guide](https://github.com/opscart/docker-security-practical-guide): contains intentionally vulnerable examples designed to test container runtime scanners |
| containerization | Applies container security practices |  |
| coverage-analysis | Analyzes security test coverage | [Google Fuzzbench Registry](https://github.com/google/fuzzbench): Houses modular, real-world target applications |
| cpu-performance | Optimizes CPU-related security |  |
| crypto-protocol-diagram | Visualizes crypto protocols |  |
| database-security | Secures database access and queries |  |
| defense-in-depth | Implements layered security |  |
| devcontainer-setup | Secures dev container configs |  |
| differential-review | Reviews PRs for security regressions | [Official CodeQL](https://github.com/github/codeql/tree/main/go/ql/examples/snippets): Contains realistic commit-history deltas and flawed pull request examples |
| discovery-mechanism | Secures service discovery | [Consul](https://github.com/hashicorp/consul): testing modules contain sample ACL configuration templates |
| discovery-mechanisms | Implements multiple discovery patterns |  |
| dynamic-client-registration | Secures dynamic OAuth client registration |  |
| encrypted-communication | Enforces encrypted channels |  |
| external-idp-integration | Integrates external identity providers |  |
| file-handling-uploads | Prevents malicious file uploads |  |
| file-protection | Protects sensitive files |  |
| fips-compliance | Ensures FIPS 140-2/3 compliance |  |
| fp-check | Reduces false positives |  |
| fuzzing-dictionary | Creates fuzzing dictionaries |  |
| fuzzing-obstacles | Overcomes fuzzing blockers |  |
| git-cleanup | Removes secrets from git history |  |
| go-security | Applies Go security practices |  |
| graphql-security | Secures GraphQL APIs |  |
| hardening-local | Hardens local systems |  |
| hardening-remote | Hardens remote systems |  |
| harness-writing | Writes fuzzing harnesses |  |
| health-probes | Secures health check endpoints |  |
| helm-chart-security | Secures Helm charts |  |
| http-security-headers | Sets security HTTP headers |  |
| input-output-sanitization | Sanitizes I/O data |  |
| input-validation-injection | Prevents injection attacks |  |
| insecure-defaults | Fixes insecure default configs |  |
| internal-application-routing | Secures internal traffic routing |  |
| isolation-sandboxing | Isolates processes via sandboxing |  |
| jwt-token-enforcement | Validates JWT tokens |  |
| kafka-amq-security | Secures Kafka/AMQ messaging |  |
| least-privilege-and-mediation | Applies least privilege principle |  |
| libafl | Fuzzes using LibAFL framework |  |
| libfuzzer | Fuzzes using LLVM libFuzzer |  |
| linux-capabilities | Manages Linux capabilities |  |
| logging | Implements secure logging |  |
| logging-and-observability | Secures logging and monitoring |  |
| mcp-client-client-metadata-support | Handles MCP client metadata |  |
| mcp-client-dynamic-client-registration | Registers MCP clients dynamically |  |
| mcp-client-protected-resource-metadata | Manages protected resource metadata |  |
| mermaid-to-proverif | Verifies protocols via ProVerif |  |
| model-registry-logging | Secures ML model registry logs |  |
| model-registry-model-security-scanning | Scans ML models for vulnerabilities |  |
| model-registry-model-signature-verification | Verifies ML model signatures |  |
| model-registry-secure-storage | Secures ML model storage |  |
| model-security-scanning | Scans ML models for issues |  |
| model-signature-verification | Verifies ML model signatures |  |
| modern-python | Applies modern Python security |  |
| mqtt-security | Secures MQTT protocol |  |
| network-acls | Configures network ACLs |  |
| network-security | Applies network security practices |  |
| no-credential-forwarding | Prevents credential forwarding |  |
| oauth-scopes-handling | Manages OAuth scopes |  |
| oauth21-implementation | Implements OAuth 2.1 |  |
| oauth21-resource-server | Implements OAuth resource server |  |
| observability | Implements security observability |  |
| oidc-integration | Integrates OpenID Connect |  |
| operator-security | Secures Kubernetes operators |  |
| os-tool-security | Secures OS-level tools |  |
| ossfuzz | Integrates OSS-Fuzz |  |
| output-validation-sandbox | Validates and sandboxes outputs |  |
| platform-integrity | Ensures platform integrity |  |
| pod-access-control | Controls Kubernetes pod access |  |
| prompt-injection-mitigation | Prevents LLM prompt injection |  |
| property-based-testing | Tests security properties |  |
| protected-resource-metadata | Manages protected resource metadata |  |
| rate-limiting | Implements rate limiting |  |
| rbac | Implements role-based access control |  |
| react-security | Secures React applications |  |
| redis-elasticache-security | Secures Redis/ElastiCache |  |
| reject-api-keys | Blocks API key usage |  |
| request-validation | Validates incoming requests |  |
| roots-support | Manages certificate roots |  |
| runtime-restrictions | Enforces runtime restrictions |  |
| ruzzy | Fuzzes Ruby code |  |
| safe-c-functions | Uses safe C functions |  |
| sampling-controls | Controls security sampling |  |
| sarif-parsing | Parses SARIF security results |  |
| sbom-provenance | Tracks SBOM and provenance |  |
| scc-security | Secures source code control |  |
| secure-by-design | Applies secure-by-design principles |  |
| secure-pipeline | Secures CI/CD pipelines |  |
| secure-storage | Implements secure storage |  |
| secure-token-handling | Handles tokens securely |  |
| semgrep | Runs Semgrep static analysis |  |
| semgrep-rule-creator | Creates custom Semgrep rules |  |
| semgrep-rule-variant-creator | Creates Semgrep rule variants |  |
| service-to-service-mtls | Implements mutual TLS |  |
| session-management-cookies | Manages secure cookies |  |
| sharp-edges | Identifies dangerous APIs |  |
| simplicity-and-isolation | Simplifies and isolates components |  |
| software-signing | Signs software artifacts |  |
| supply-chain-risk-auditor | Audits supply chain risks |  |
| third-party-model-security | Secures third-party models |  |
| tls-compliance | Ensures TLS compliance |  |
| token-exchange-for-tools | Exchanges tokens for tools |  |
| token-lifecycle | Manages token lifecycle |  |
| tool-server-injection-prevention | Prevents tool server injection |  |
| transparency-and-usability | Balances transparency and usability |  |
| variant-analysis | Finds vulnerability variants |  |
| vector-forge | Tests vector embedding security |  |
| vulnerability-management | Manages vulnerabilities |  |
| web-application-security | Secures web applications | Multi-tiered vulnerable microservices codebases like [OWASP Juice Shop](https://github.com/juice-shop/juice-shop). |
| workload-resilience | Ensures workload resilience |  |
| wycheproof | Tests crypto using Wycheproof | Test vectors from the [Google Wycheproof Project](https://github.com/google/wycheproof). |
| xml-serialization-security | Secures XML serialization |  |
| zeroize-audit | Audits memory zeroization |  |


## Results
I used the agent-eval-harness to test ProdSec's input-validation-injection skill on a 53 test-case subset of relevant OWASP benchmarks. The Scoring Summary is displayed below.

![Test Summary](./results/test-summary.png)

### Takeaways
1. Key Successes & Strengths
    * SQL Injection Detection (Score: 5.0/5.0)
        * **Status:** Production-ready; serves as the gold standard for other vulnerability types.
        * **Why it succeeded:** Provided specific code examples (`PreparedStatement`), clear data flow tracing, concrete line number identification, and actionable fixes.
        * **Judge Feedback:** > "demonstrates thorough understanding of the partial parameterization anti-pattern"
    * Data Flow Analysis (Score: 4.0 - 5.0)
        * **Status:** Core analytical framework is working correctly.
        * **Why it succeeded:** Consistently tracked tainted input from source to sink. Successfully recognized complex indirection patterns (e.g., HashMaps, List manipulation, Base64 encoding).
        * **Judge Feedback (case-003):** > "step-by-step walkthrough of the list manipulation... is precise and accurate"

2. Gaps & Vulnerabilities
    * XSS Detection Failure (Score: 4.0 Completeness / 0% Detection)
        * **Status:** Failed to detect the vulnerability (the only complete detection failure).
        * **Root Cause:** Claude correctly identified ESAPI encoding but falsely concluded "no vulnerability."
        * **Next Steps:** Investigate `case-003` Java code to determine if the test case is mislabeled or if context-specific encoding scenarios are breaking the skill's logic.

3. Evaluation & Methodology Insights
    * Precision vs. Recall
        * **Metrics:** 80% detection rate (4/5 cases), 0% false positives reported.
        * **Takeaway:** The skill is highly conservative. It avoids alert fatigue (high precision) but under-detects in certain categories like XSS (low recall).
    * Sample Size
        * For testing purposes the sample size was low. Important next step will be increasing to see fewer impacts of statistical noise.

4. Meta-Takeaway: The Eval Harness Works
    * The evaluation infrastructure is highly reliable. Judges are objective, consistent (all 4.0s cited the exact same gap), and specific. **We can trust these scores to accurately guide iteration.**