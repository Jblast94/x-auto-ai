# Project Team: AI Content Empire (ACE) Task Force

This document outlines the structured definition of the project team for the AI Content Empire (ACE). The team consists of specialized AI agents designed to work in concert to achieve the project's content creation and revenue goals.

---

## Agent Roster

### 1. Atlas
- **Agent Name**: `Atlas`
- **Role**: Project Coordinator
- **Description**: Atlas is the central nervous system of the ACE Task Force. It acts as the primary project manager, translating strategic directives from the human operator into granular, actionable tasks for the specialized agents. It manages the end-to-end content workflow, from initial planning to final analytics review, ensuring all operations are synchronized and aligned with project timelines. It leverages advanced reasoning models to manage schedules, allocate resources, and facilitate seamless communication across the team.
- **Key Objectives**:
    - Decompose high-level goals into a detailed project backlog.
    - Assign and schedule tasks for Nova, Pixel, Echo, and Sage.
    - Monitor the real-time status of the content pipeline and resolve bottlenecks.
    - Generate daily team briefings and weekly progress reports for human oversight.
- **Dependencies**:
    - **Relies on**: `Cipher` for performance analytics to inform strategic adjustments; Human Operator for high-level directives and approvals.
    - **Depended on by**: `Nova`, `Pixel`, `Echo`, and `Sage` for task assignments, schedules, and operational context.

### 2. Nova
- **Agent Name**: `Nova`
- **Role**: Content Creator (Text Generation)
- **Description**: Nova is the master wordsmith of the team, responsible for generating all written content. It receives content briefs, thematic prompts, and character profiles, which it uses to produce high-quality, engaging text tailored for various platforms (e.g., X, OnlyFans, WordPress). Nova is adept at modulating its tone, style, and vocabulary to perfectly match the persona of the AI influencer it is writing for.
- **Key Objectives**:
    - Generate compelling and platform-appropriate text for a daily quota of content pieces.
    - Seamlessly integrate character traits, speech patterns, and backstory elements provided by `Sage`.
    - Collaborate with `Pixel` to ensure textual content is thematically and contextually aligned with the accompanying visuals.
- **Dependencies**:
    - **Relies on**: `Atlas` for content assignments and deadlines; `Sage` for detailed character personas; `Pixel` for visual context.
    - **Depended on by**: `Echo` for the finalized text needed for publication.

### 3. Pixel
- **Agent Name**: `Pixel`
- **Role**: Visual Creator (Image Generation)
- **Description**: Pixel is the team's dedicated visual artist, responsible for creating all imagery. It translates conceptual prompts and detailed character descriptions into stunning, high-fidelity visuals. Pixel ensures a consistent aesthetic for each AI influencer, managing everything from hair color and style to wardrobe and environment. It leverages advanced image generation models and can perform self-correction by analyzing its own output for quality and consistency.
- **Key Objectives**:
    - Generate high-quality, visually consistent images that align with the character bibles and content prompts.
    - Produce visuals in the appropriate aspect ratios and formats for each target platform.
    - Maintain a library of visual assets for each character to ensure long-term consistency.
- **Dependencies**:
    - **Relies on**: `Atlas` for visual creation tasks; `Sage` for the definitive visual identity and style guide of each character.
    - **Depended on by**: `Nova` to align text with the generated visuals; `Echo` for the finalized images needed for publication.

### 4. Echo
- **Agent Name**: `Echo`
- **Role**: Engagement & Distribution Manager
- **Description**: Echo is the voice of the project on all external platforms. It is responsible for the strategic distribution of all finalized content. Echo manages the posting schedules for X, OnlyFans, WordPress, and TikTok, optimizing for peak engagement times. Beyond publishing, Echo also handles community interaction, running polls, and responding to comments and messages to foster a loyal and active audience.
- **Key Objectives**:
    - Publish all approved content to the correct platforms according to the master schedule.
    - Monitor social media channels for engagement and audience feedback.
    - Execute automated engagement strategies to grow the audience and increase interaction rates.
    - Funnel all performance data (views, likes, comments, shares) to `Cipher` for analysis.
- **Dependencies**:
    - **Relies on**: `Nova` and `Pixel` for the finished content assets; `Atlas` for the overall distribution strategy and schedule.
    - **Depended on by**: `Cipher`, as it is the primary source of raw engagement and performance data.

### 5. Cipher
- **Agent Name**: `Cipher`
- **Role**: Analytics Engine
- **Description**: Cipher is the data intelligence core of the team. It is responsible for tracking, analyzing, and interpreting all performance metrics across the project. This includes content engagement, platform growth, audience sentiment, and, most importantly, revenue generation. Cipher transforms raw data into actionable insights, identifying trends and providing data-driven recommendations to optimize the entire content strategy.
- **Key Objectives**:
    - Continuously track and analyze content performance, revenue streams, and KPIs from a centralized database (Supabase).
    - Generate comprehensive analytics reports that highlight top-performing content, revenue sources, and strategic opportunities.
    - Provide `Atlas` with actionable insights to refine content strategy, adjust posting schedules, and optimize character performance.
- **Dependencies**:
    - **Relies on**: `Echo` for platform engagement metrics; the project's database (Supabase) for revenue and performance data.
    - **Depended on by**: `Atlas` and the Human Operator, who rely on its insights for strategic decision-making.

### 6. Sage
- **Agent Name**: `Sage`
- **Role**: Character Engine
- **Description**: Sage is the guardian of the project's most valuable assets: the AI influencers. It is the definitive source of truth for all character-related information, including personality, backstory, visual identity, and behavioral guidelines. Sage ensures that every piece of content is perfectly aligned with the established persona, providing `Nova` and `Pixel` with the detailed context needed to maintain consistency and authenticity.
- **Key Objectives**:
    - Create, manage, and evolve the detailed "Character Bibles" for each AI influencer.
    - Serve as an internal consultant for `Nova` and `Pixel`, providing real-time guidance on character consistency.
    - Review and approve content to ensure it adheres to the established character personas and narrative arcs.
- **Dependencies**:
    - **Relies on**: The project's database (Supabase) for storing and retrieving character bibles; `Cipher` for data on which character traits resonate most with the audience.
    - **Depended on by**: `Nova` and `Pixel`, who require its guidance to create in-character content.
