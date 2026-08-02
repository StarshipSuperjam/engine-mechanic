# Platform capability baseline — the approved snapshot

*The denominator. Adopted by [decision 0332](../../adr/0332-adopt-the-platform-capability-baseline-snapshot-and-comparis.md);
every future platform-currency run diffs against this snapshot under [comparison-rules.md](comparison-rules.md),
and it is replaced only by a new recorded decision — never refreshed in place.*

- **Audit date:** 2026-08-02 (all sources fetched, all fingerprints taken, same day).
- **Repository reconciled against:** engine-template @ `cdbbc3357fbfbc192005650a8be6ce35b7942bfe` (HEAD at
  audit time, identical to the spec corpus's reconciliation pin).
- **Corpus:** 247 capability records (184 claude, 55 codex, 8 models) across the three catalogs; 107 unique
  cited sources, all on the approved origin allowlist.
- **Version observations at snapshot time:** Claude Code CHANGELOG head ≈ v2.1.220 (audit-prep pins 2.1.176);
  Codex CLI latest release 0.146.0 (0.147.0-alpha series unread — partial page); Claude Agent SDK Python
  0.2.128 / TypeScript 0.3.220; Anthropic lineup per catalog-models (Fable 5 / Opus 5 / Sonnet 5 /
  Haiku 4.5 current; Opus 4.1 retiring 2026-08-05); OpenAI lineup per catalog-models (GPT-5.6 Sol/Terra/Luna;
  gpt-5.4/-mini retiring from Codex 2026-08-31).
- **Fingerprint method:** sha256 of the raw HTTP response body of each cited URL, fetched 2026-08-02 by the
  audit session (curl, redirects followed). Client-rendered pages hash their served shell, so a changed hash
  means "the served document changed", not necessarily "the documented capability changed" — the comparison
  rules treat a fingerprint delta as a *prompt to re-read*, never as a finding by itself.
- **Known source-map corrections for the next run:** `developers.openai.com/codex/local-and-cloud` redirects
  to a 404; `developers.openai.com/codex/web` misroutes to general ChatGPT docs (the Codex web surface is
  documented within `/codex/cloud`).

## Source fingerprints

| Source (fetched 2026-08-02) | sha256 | bytes |
| --- | --- | --- |
| https://agents.md | `aa6fbda823099086a550…` | 81690 |
| https://code.claude.com/docs/en/agent-sdk/claude-code-features | `c116edab9d165b3f808e…` | 533943 |
| https://code.claude.com/docs/en/agent-sdk/custom-tools | `f5657063c89b04d46d8c…` | 936224 |
| https://code.claude.com/docs/en/agent-sdk/hooks | `aae6a62222ab0738fb7b…` | 937576 |
| https://agents.md | `aa6fbda823099086a550048ff638136c05077f3da03f061fea8de154059550a8` | 81690 |
| https://code.claude.com/docs/en/agent-sdk/claude-code-features | `c116edab9d165b3f808e1248d39e146bd245916ee568e8998db51c9ef55de4e2` | 533943 |
| https://code.claude.com/docs/en/agent-sdk/custom-tools | `f5657063c89b04d46d8c4ef2dc0babf5426b6110a0e3c12fde984b18f9456c21` | 936224 |
| https://code.claude.com/docs/en/agent-sdk/hooks | `aae6a62222ab0738fb7bd0356bb07a737407b423375369232525e8473b077dc9` | 937576 |
| https://code.claude.com/docs/en/agent-sdk/mcp | `049f77c8a3c45a6b2094e438dfb4c4a40550d54902259806f86c0e01340da1ce` | 968890 |
| https://code.claude.com/docs/en/agent-sdk/overview | `e6aa2cb5e92ec28ca4f1d4e88c1d2ff57b802f15c488d4b6c4b9ee16f4752336` | 351054 |
| https://code.claude.com/docs/en/agent-sdk/permissions | `3da6697be6a3cc92d7c2ec8c3d1788d0dc5604a31f67e4e387af0d5d18590a57` | 480353 |
| https://code.claude.com/docs/en/agent-sdk/sessions | `feae4c1178c7b8739f8597f78c814d9687e91663240f99ac6100d1796cc2f537` | 588151 |
| https://code.claude.com/docs/en/agent-sdk/subagents | `bb43f12501f7d4c792e86469f273fbba468324b0252c4118531fa79d4e67c2b3` | 760384 |
| https://code.claude.com/docs/en/agent-sdk/user-input | `e32fe8177398c310d0955a951b301546de491fd5faac6578770a049d58fb7571` | 965050 |
| https://code.claude.com/docs/en/agent-teams | `5876d34b5f84a912d1b80a1c21de676560c1704478c4c703eb435e0faabac05e` | 607995 |
| https://code.claude.com/docs/en/agent-view | `02ddc85911d37a8ef0491c0e468d29b39cc50e413d65025954426e1e3dc83a47` | 820430 |
| https://code.claude.com/docs/en/checkpointing | `1101cbf13a6b1d4cc543f160b23f1934e3b10798143b43f0bae8a5c046c3ca9e` | 353056 |
| https://code.claude.com/docs/en/chrome | `b1a501789ecbcff22f6ba4ad7e9c0f0e3531605e7b0ae726f74b0149a3b2ee57` | 497371 |
| https://code.claude.com/docs/en/claude-code-on-the-web | `b7584e9f47bafbb2205915e54881fa16b495197c9cbd57c51d7320964546e6a3` | 505647 |
| https://code.claude.com/docs/en/cli-reference | `db0e0a08ea93d6f2db4788133d1ccf5affeb6562a781696f265765003215e1e7` | 428647 |
| https://code.claude.com/docs/en/cloud-environments | `d89dae85ce546313ec47a6752c5ec8e5b2f3284dfbdb4b093282e60ecd43afa7` | 605178 |
| https://code.claude.com/docs/en/code-review | `00f72939b7e3ba93c43bbb27e1cfc63ce4ee68650a49500392a2d1de63f0f167` | 496968 |
| https://code.claude.com/docs/en/commands | `47c12302dd35d87db77dc230407eef3a99779f25d1a38fcb7ac7c41407989dc7` | 427921 |
| https://code.claude.com/docs/en/computer-use | `7f0e4d5f9fa7507c423d722fbd80164c321853f1969286cabf90c58571d95697` | 436388 |
| https://code.claude.com/docs/en/costs | `ff0e62026e0e389a134bfc6c67ba26ccdcd22c05988237f41fa2874bb8550271` | 504718 |
| https://code.claude.com/docs/en/desktop | `c2c1635620106e19497f3b8b00795b1881a32bb8828b5213247563e1143ef34d` | 866484 |
| https://code.claude.com/docs/en/desktop-quickstart | `9e3c3e5d6941a9cf23415288a576f55e914a4c4526e6c2282d3e8fedd779e7f2` | 372401 |
| https://code.claude.com/docs/en/desktop-scheduled-tasks | `55f759a14d64b8d7d6608de27bdd968dbd8de91b4a2e8854134c6f3f475dc068` | 371613 |
| https://code.claude.com/docs/en/github-actions | `9609bffd15e14067462ba81c9a53088b8381777acfa05e4725d612588c8ec996` | 659578 |
| https://code.claude.com/docs/en/headless | `d91c44d1310743a15b53afc5819418bd2aa2a9f9e9164e04435f4f67cf16650c` | 561795 |
| https://code.claude.com/docs/en/hooks | `208f7fdf9c3344c3f6e94bd17e833bff8a7299fb274a2a478c626e366e699593` | 2432916 |
| https://code.claude.com/docs/en/hooks-guide | `be91397774c7c7697b5f78872236b42ccc3b4940b739558be81d8aafe9fcb474` | 962264 |
| https://code.claude.com/docs/en/iam | `6a183856420150a8f7738b0a86518068849ff19411c23117b57b8399b0fdd501` | 411148 |
| https://code.claude.com/docs/en/interactive-mode | `64e8be1720a2dfe4a7c23719bcd9189375fcc727b1b6c38f9e723dcc8646db1e` | 525300 |
| https://code.claude.com/docs/en/jetbrains | `1f26f4e3ce66105d621cd70d3e043f5180005f14bd4a3582103ec62576819e59` | 444365 |
| https://code.claude.com/docs/en/managed-mcp | `6ff3789f0b46f4a207e9fdd4ff13b24f9fe347182e9f2b0c6229e1bfc9fe8e21` | 556558 |
| https://code.claude.com/docs/en/mcp | `03fb72ba7f54f06421cf5ed3bd9fb07df096aedad8b8ae329faa3da976cbacf1` | 1255719 |
| https://code.claude.com/docs/en/mcp-quickstart | `efac716d7723893af2201354d4ece5813277cadfdcf9cedaae62e606debba104` | 591184 |
| https://code.claude.com/docs/en/memory | `c7718dc6b9f4b1b6d2d3d071eb9cb14625ce4cb08b8c7e9469386864cfd2620e` | 601575 |
| https://code.claude.com/docs/en/model-config | `0909c6b896c5f8d20a205864c054a67cc3f8adb31600c59628912f50207645ed` | 866621 |
| https://code.claude.com/docs/en/output-styles | `056c1f544640358f9275d30be3ae780c461d8575bcf66511ab8612de07d8c16c` | 360672 |
| https://code.claude.com/docs/en/overview | `bdec72e9e7e97274a6464daa1d5ffa73509be87d77988ea7d0771af84afe50b9` | 468136 |
| https://code.claude.com/docs/en/permission-modes | `83dbd10afa800323aae4412de5b2e573a51bdbc1837da06f6458852cecbc40b2` | 571007 |
| https://code.claude.com/docs/en/permissions | `a78c502a4ae2b1a302cb56ac66a486e610f4c35dbc4c957fb5f8a53026fdc363` | 611508 |
| https://code.claude.com/docs/en/plugin-marketplaces | `bcb0e49156f68e977833c180ce0356c4f72c2f003c6d7719c96ec9be79f2837b` | 1184755 |
| https://code.claude.com/docs/en/plugins | `a8d0bde0c23349221ecf764e5e76c2a161bf357033959badc4e9be8fbba89e0f` | 676225 |
| https://code.claude.com/docs/en/remote-control | `4d584b7f710abe7df1a9e7b495f53fb882ef664e7a126d439c314a4efa134297` | 547664 |
| https://code.claude.com/docs/en/routines | `bab4f8e2d153702558e9726fb312f3bc4bb29059c8ee9ece7d8f0abb292b8065` | 523808 |
| https://code.claude.com/docs/en/sandboxing | `b98556602d50d106d39461ead7db66d88dc6a43e178e38d762457c6ffdb25ac5` | 624557 |
| https://code.claude.com/docs/en/scheduled-tasks | `26756a2429b34bac497a04aa39f92e7d56173ce099efb9d7424d189af8eb1378` | 464377 |
| https://code.claude.com/docs/en/sessions | `f1c26bd0ecab7c6256c911ac1d3938607b686fef94cb985a64123b13e63f67d8` | 428373 |
| https://code.claude.com/docs/en/settings | `66ec51c0eb3192b662b1d9b10d085da56efe8bc9aa3ae6363eefce7a25b966c7` | 1190685 |
| https://code.claude.com/docs/en/skills | `aa66a89a12b406a089b3afd6212a2a48ebed80f9a5b2476c0591178fa066b6e4` | 943476 |
| https://code.claude.com/docs/en/statusline | `e60aea7f0e9c7d731c9c53b7415a435d03be6a756395811fe9639132f2b8d7e8` | 1309367 |
| https://code.claude.com/docs/en/sub-agents | `995a3d785d95b53a5703e040cde77ed9510ac0240b3519ad275b9ee189df80f7` | 1092898 |
| https://code.claude.com/docs/en/tools-reference | `f168cf24337ad0f8ab98faaf1057059684f01b2b59e4887fe7aa774f6ef0573b` | 532029 |
| https://code.claude.com/docs/en/ultrareview | `46769ade3d7e08be11b9a735e495ff7ec63c664448cb84dd61aca0bc75a8209d` | 415380 |
| https://code.claude.com/docs/en/vs-code | `23b320a8796e50a3f3e58cf2cfee24d42837bd5a7d9f80b07f3a237854a7b920` | 656451 |
| https://code.claude.com/docs/en/worktrees | `4e5ba9f073e2ffa6f10ff365d3f90ad42e909ca1e3b5e5af3bad49bbd91e490b` | 503950 |
| https://developers.openai.com/api/docs/deprecations | `a2910e7110a7e8dc729fdc406dd9b661303b477374c40885caaffab0d8ca682f` | 442794 |
| https://developers.openai.com/api/docs/models | `60801b818e1fc32164867a1da4837abf652a2b535b1cb99d2e56148427547043` | 339172 |
| https://developers.openai.com/codex/automations | `67442eea76f01cf12d8c003d3395c97a0e2a23ff41e36e9d2e5c22b1e7142ec9` | 432477 |
| https://developers.openai.com/codex/changelog | `48616cf688b59ebb4a509c730e0d5597d9c70dc1d3725da1c25a6738c0ef97bd` | 611579 |
| https://developers.openai.com/codex/cli | `c9fc12a41f9178d3848902f2f7664903576639258e1b44d8e1d15671402f8338` | 362637 |
| https://developers.openai.com/codex/cli/reference | `361ce63c00b179bf736815e82da3a79566f23eca157ad2bc8362afa45e4b3e48` | 1034178 |
| https://developers.openai.com/codex/cli/slash-commands | `361ce63c00b179bf736815e82da3a79566f23eca157ad2bc8362afa45e4b3e48` | 1034178 |
| https://developers.openai.com/codex/cloud | `62f07d820b29d9a131d414e4487fd37087a06dface38d6ee78b959d5454b8d77` | 358846 |
| https://developers.openai.com/codex/code-review | `7c927a174bfd362b5c6d21d1571c78f04d88607ae89fff2b33a577374104f97c` | 449412 |
| https://developers.openai.com/codex/concepts/sandboxing/ | `b95570e6a0c6e84319c2e2beb56f81bff350c5b069fa0de97eed19bf9ee47b4f` | 404751 |
| https://developers.openai.com/codex/config-file/config-reference | `0befe59b21783c52fd28540390600f8f1b3842dd375fa1b401a3de375920185a` | 1220725 |
| https://developers.openai.com/codex/developer-settings | `725d5b842085223384b8fa5d820ef5968f5917496b0db7213b9d32ff2dbaf125` | 371172 |
| https://developers.openai.com/codex/extend/mcp | `51cf58e5758a51bd592e2a085a64a5b1b7c9b1482c72d74eb0752f46910fb9a6` | 411956 |
| https://developers.openai.com/codex/feature-maturity | `c3b496c97c56c4ee6b76c0f8745f373beec6bf4debc9cda0bd8ca268136edc5a` | 294139 |
| https://developers.openai.com/codex/ide | `e1f258071782103c04d45a687bbd8b077d24fdd8b2dd1428d867865d1c08de8c` | 408545 |
| https://developers.openai.com/codex/integrations/github | `4b53111e3d4ea000d09c2e5ee2630079f11d4af61840dec4413a7878f0d62c0a` | 318804 |
| https://developers.openai.com/codex/noninteractive | `05535c82f4c79e16e31e9c7f822f7048b0ac19396bfbd44acd82eb59b5b21a60` | 386599 |
| https://developers.openai.com/codex/permission-modes | `038015ca4a343c55c463aa3e73dbdffd3877e39e080fbaed2d865ad562d399f2` | 329545 |
| https://developers.openai.com/codex/permissions | `9b98761dec9df1fde0be0804d87f2d0cd102b68e905a36d357cd9bab19a55e55` | 402450 |
| https://developers.openai.com/codex/sdk | `531f49f08bb70e03579d046fe51f1850c1195a34a2cac47a0b2d7371f08410df` | 324767 |
| https://developers.openai.com/codex/use-cases/github-code-reviews | `06b71193d13a76104d639d101efba43450716d1813748a41db32990dcacaac79` | 316370 |
| https://github.com/openai/codex/releases | `95d32cce36ace0701caf8d0f9d200c7185472382fe192979d2b1c7bfe546d48d` | 562777 |
| https://github.com/openai/codex/tree/main/sdk/typescript | `5ad5375bdb5da2cb7eac49f179eb06cf25ecec280b9e561a98eacf232be739f5` | 338675 |
| https://learn.chatgpt.com/docs/agent-configuration/agents-md | `3f3c79f1a29a0f6b419e4980007cdd523b73571e46959fb77771dc16d7bb9c9f` | 349143 |
| https://learn.chatgpt.com/docs/build-skills | `6f9982ac4d5cefbceaced6f9dedaa3580ea8894046ebb7351b848251ea403434` | 343481 |
| https://learn.chatgpt.com/docs/changelog | `48616cf688b59ebb4a509c730e0d5597d9c70dc1d3725da1c25a6738c0ef97bd` | 611579 |
| https://learn.chatgpt.com/docs/cloud/internet-access | `34a5cad8eac75d57fdfb5b603e9cddf16e7587131b332e53b11f048c6f56b624` | 319045 |
| https://learn.chatgpt.com/docs/config-file/config-basic | `5cef4d0c52ca301a8e44e892bd01ebeafe1f0dbfcdc817e38fbb3ee83883858b` | 367366 |
| https://learn.chatgpt.com/docs/config-file/config-reference | `0befe59b21783c52fd28540390600f8f1b3842dd375fa1b401a3de375920185a` | 1220725 |
| https://learn.chatgpt.com/docs/custom-prompts | `29a2b78f13045965945f9a5c68673c167ea42b02e539723085b9e7ddd02b62fd` | 303907 |
| https://learn.chatgpt.com/docs/enterprise/admin-setup | `0d1e1b7380ed58f2fb9be2a1f010fa9f84692eb8e79b43713e348c750ceed693` | 323974 |
| https://learn.chatgpt.com/docs/environments/cloud-environment | `f6d4127d5aeab1dba3b3144f4a3fc4cfefb5dc347cb4b0e71aed1df5a57fe400` | 318385 |
| https://learn.chatgpt.com/docs/environments/git-worktrees | `1ba657ca4ab498025a9fb29d4917370b77d1b98cf879b13f5dbc248ed2757988` | 354883 |
| https://learn.chatgpt.com/docs/models | `1184508c6f25dfdfaa937a11e12102786dd47c7877c99f873196c4c195b9816d` | 602544 |
| https://learn.chatgpt.com/docs/remote-connections | `620c57edfe1de6526a701d97730841f0c2d475f75b557938f0923d16d2186503` | 379664 |
| https://platform.claude.com/docs/en/about-claude/model-deprecations | `6d0918947d9a6356f918a383e7f8659dfdd96765369e3a93282186a8342c69b4` | 853603 |
| https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions | `1909713b96cb5f0a0f1612d97b0cbb87ae03b7846f8a70d6e6cf70366dfd2571` | 742318 |
| https://platform.claude.com/docs/en/about-claude/models/overview | `9cc841ef6a34c2a35f1f90a7c96ab17b6339b3ce7725271e7a126cb94088a3c0` | 837097 |
| https://platform.claude.com/docs/en/about-claude/pricing | `6b9f5f12c1506765f003ebf62091fba7c30fc07a5c87d98329a28e458974d49a` | 1032310 |
| https://platform.claude.com/docs/en/build-with-claude/effort | `150e9fdc76247200712f955643e7b747fe2b27b2923c59f9616fc0f1cdba572d` | 948739 |
| https://platform.claude.com/docs/en/managed-agents/overview | `affb6f8f0d25e09920e526d034c1cc47bad1970e7fe10f2d848d96822c1bf387` | 779707 |
| https://platform.claude.com/docs/en/release-notes/overview | `6652aa4d543ac37379b2734faefbef7fb41237d26d8fbac87c89176f0549b5a5` | 1439386 |
| https://raw.githubusercontent.com/anthropics/claude-agent-sdk-python/main/CHANGELOG.md | `e53ce0c6c55070095602e6a586051d0b07e627c59f704c3d55d6830c5fa20509` | 48163 |
| https://raw.githubusercontent.com/anthropics/claude-agent-sdk-typescript/main/CHANGELOG.md | `d1c387b8e19e09d2402fc09f87f6d0ceef13aac0cc6a75accb5e1746a0bb5a6c` | 52945 |
| https://raw.githubusercontent.com/anthropics/claude-code-action/main/README.md | `a381c47399445c97480d025a406f485644fdd5f4f7ffd880be0567ac2f7b4640` | 4896 |
| https://raw.githubusercontent.com/anthropics/claude-code-action/main/action.yml | `87ca609725e2a8dbbffa82c3610b6ff741d7fcabf54c74d69a7a11c0123bdbde` | 22962 |
| https://raw.githubusercontent.com/anthropics/claude-code-action/main/docs/usage.md | `70f62d0f2f42b9b1945e42ea064debcdfdb7aae0ad6c784ca9a984254327633f` | 21275 |
| https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md | `9e4ad11b0443ad9db409b030481e284eb819781d94ee9f1ad28844b7759d74f5` | 477054 |
| https://support.claude.com/en/articles/12012173-getting-started-with-claude-in-chrome | `f08d1e68bcc60937fdff69acde44f33bf050a3287b9543fdcd9dfad39d6c63a8` | 142374 |
| https://support.claude.com/en/articles/12138966-release-notes | `3a5d38d7ec7888181f503bd4a47110a698acb62653a2b48f01e9dee80c790c23` | 241413 |
| https://support.claude.com/en/articles/12902428-using-claude-in-chrome-safely | `33b6b34d3d4af800991167cf5b047236781fe5e00061549924b85481ac94d612` | 130361 |
| https://support.claude.com/en/articles/13065128-claude-in-chrome-admin-controls | `3993dfcf4feaa5f524d39c73289656561b30a475fb1991eb1324643c1b8862fb` | 124182 |
