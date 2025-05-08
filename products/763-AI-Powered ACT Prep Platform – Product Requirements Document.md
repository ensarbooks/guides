# AI-Powered ACT Prep Platform – Product Requirements Document

## Overview and Purpose

The **AI-Powered ACT Prep Platform** is a Software-as-a-Service (SaaS) product designed to generate and deliver personalized ACT exam preparation content using artificial intelligence. Its core purpose is to help students prepare for the ACT by automatically creating high-quality practice questions, full-length mock exams, customized study plans, and detailed answer explanations. By leveraging AI, the platform aims to **provide a scalable, adaptive, and engaging test prep experience** that adjusts to each learner’s needs. Key outcomes of this platform include improving students’ ACT scores, saving educators time in content creation, and providing actionable insights through analytics.

**Scope:** This document outlines the comprehensive product requirements for the platform, targeting product managers responsible for planning and implementing the system. It covers the platform’s intended users and personas, detailed feature set, user roles and permissions, functional and non-functional requirements, technical architecture, integrations, UI/UX design considerations (including wireframes for major workflows), success metrics, and compliance needs. By the end of this document, product managers should have a clear blueprint of the platform to effectively communicate to stakeholders and guide the development team.

**Key Objectives:**

- Use AI to **generate ACT-aligned content** (questions, exams, explanations) at scale, maintaining quality and relevance to the ACT exam format and standards.
- **Personalize learning** through adaptive difficulty and tailored study plans, addressing each student’s strengths and weaknesses.
- Provide **rich analytics and progress tracking** for students, teachers, and administrators to monitor performance and guide interventions.
- Support multiple **user types (students, teachers, school admins, content managers)** with appropriate roles and permissions, ensuring each has an interface and tools tailored to their goals.
- Ensure the platform is **secure, scalable, and reliable**, able to support potentially thousands of users and large content generation tasks with high performance.
- Integrate with existing educational systems and uphold all relevant **educational standards and data privacy regulations** to fit seamlessly into school or tutoring environments.

The sections below detail each aspect of the product requirements to ensure clarity and completeness for implementation.

## Target Users and Personas

The platform serves a variety of users in the education space, primarily focused on high school ACT preparation. Key target user groups include **students preparing for the ACT**, **teachers or tutors** assisting students, **school administrators or tutoring company managers** overseeing programs, and **content managers or curriculum designers** who maintain the learning materials. For each group, we define user personas to illustrate their needs, motivations, and how they will interact with the platform.

### Primary User Groups

- **Students:** High school juniors or seniors (typically ages 16–18) who plan to take the ACT. They may be self-driven or guided by educators. These users want engaging practice material, feedback on their performance, and a clear study plan to reach their target ACT scores.
- **Teachers/Tutors:** Educators in schools or private tutoring companies who help students prepare. They seek high-quality content without having to create it all manually, tools to track student progress, and the ability to personalize assignments to each student’s needs.
- **School Administrators/Tutoring Managers:** Decision-makers (e.g. a school’s head of curriculum or a tutoring center’s director) who implement the platform for a group of students. They need oversight of all student and teacher activities, aggregated results to measure program effectiveness, and assurances of content quality and compliance with standards.
- **Content Managers/Curriculum Designers:** Education content specialists (possibly within the company providing the platform or within a school) responsible for the question bank and study materials. They focus on reviewing AI-generated content for accuracy, aligning materials with ACT standards, and curating the content library.

### User Personas

To better understand user needs, we outline detailed personas for each group:

**1. Student Persona – “Alex the Ambitious Junior”**

- **Profile:** 17-year-old high school junior aiming for a top university. Currently scoring around 25 on ACT practice tests, but aiming for 32+. Busy with school and extracurricular activities.
- **Goals:** Improve ACT score by at least 7 points, identify weak areas (e.g. Science section or specific math topics) and focus on them, practice regularly despite a busy schedule, and build test-taking confidence.
- **Pain Points:** Limited time to study, overwhelmed by where to start, difficulty finding quality practice questions at the right difficulty. Needs guidance on what to study each week.
- **How the Platform Helps:** Provides a personalized study plan that fits around Alex’s schedule, adaptive practice that gives harder questions as he improves (and easier ones when struggling) to keep him challenged, and instant explanations so he can learn from mistakes. The AI tutor feature allows Alex to ask follow-up questions when he doesn’t understand a solution, simulating a one-on-one tutor experience. Progress dashboards motivate Alex by showing improvement over time and projecting his potential ACT score range.

**2. Teacher Persona – “Beth the Busy Tutor”**

- **Profile:** 30-year-old professional tutor who coaches small groups for the ACT. Works with 20 students at varying skill levels. Tech-savvy but has limited time to prepare custom materials for each student.
- **Goals:** Efficiently assign practice tests and questions tailored to each student’s level, monitor all her students’ progress in one place, and pinpoint where each student needs help (e.g. if several students are struggling with algebra). Save time on grading and explanation by using the platform’s auto-generated solutions.
- **Pain Points:** Creating diverse practice questions and full exams manually is time-consuming. It’s hard to keep students engaged and track who has done what. Needs to justify progress to parents and her tutoring company with data.
- **How the Platform Helps:** Beth uses the platform’s **question generation** to produce new practice sets without writing them herself. She can generate full-length ACT-like exams on demand for her group. The platform’s **analytics dashboard** shows each student’s scores, time spent, and problem areas at a glance. She can drill down to see, for example, that Student A struggles with geometry, while Student B needs reading speed improvement. With adaptive difficulty, the system gives each student appropriately challenging questions automatically. Beth can also add her own custom questions or review the AI’s questions via a content manager interface if needed, ensuring everything aligns with what she taught. The **explanation** feature means she spends less time writing out why answers are correct; instead, she can focus on discussing strategies with students, using the provided explanations as a guide.

**3. Administrator Persona – “Carlos the Curriculum Coordinator”**

- **Profile:** 45-year-old district curriculum coordinator at a high school. Evaluates and implements educational software for test prep. Not directly teaching, but oversees teachers and student outcomes. Concerned about both effectiveness and compliance (data privacy, alignment to standards).
- **Goals:** Ensure the ACT prep program improves student scores across the school, demonstrate ROI of the platform (e.g. higher average ACT scores or more students meeting benchmarks), and make sure the content used is high-quality and matches ACT curriculum standards. Needs high-level reports and the ability to manage teacher and student accounts easily.
- **Pain Points:** Hard to aggregate results from different classes or tutoring programs. Worried about consistency of practice material quality. Also must ensure student data is secure and that using an AI tool complies with privacy laws and school policies.
- **How the Platform Helps:** Carlos gets an **admin dashboard** with summary statistics – e.g., average score improvements per quarter, number of practice tests taken school-wide, usage rates. He can manage user accounts (invite new teachers, reset passwords, etc.) and set permissions. The platform assures him that content is aligned with ACT College and Career Readiness Standards and has been reviewed by experts (or vetted AI) for accuracy. Integration with the school’s LMS means students and teachers can sign in with existing school accounts (simplifying IT management). Automated data privacy compliance features (like anonymizing student IDs in reports, or obtaining necessary consents) put Carlos at ease with adopting the AI-driven solution.

**4. Content Manager Persona – “Dana the Content Developer”**

- **Profile:** 28-year-old content developer working for the platform provider (or at a large tutoring company). Background in education and test prep. Not a programmer, but comfortable with content management systems.
- **Goals:** Maintain a **large and diverse question bank** that covers all ACT topics (English, Math, Reading, Science, plus optional Writing prompts) at varying difficulty levels. Use AI to generate new questions and explanations, but ensure they meet quality standards before they reach students. Continuously update content to reflect any changes in the ACT (e.g. new formats or standards).
- **Pain Points:** Generating fresh content manually is slow; however, relying purely on AI can introduce errors or off-syllabus questions. Needs a workflow to efficiently review AI outputs. Also must organize content (tag by topic, difficulty, etc.) so that the adaptive system can pull the right questions.
- **How the Platform Helps:** Dana uses a **Content Management Module** where she can input parameters (e.g. generate 50 algebra questions of medium difficulty) and the AI will draft them. She then reviews each question in an interface that shows the AI-suggested question, options, and the correct answer with explanation. If she spots an issue (maybe the AI’s question is too ambiguous or not aligned with ACT style), she edits or regenerates it. The system might highlight content with potential problems for her (e.g. flagged by an AI content filter for potentially sensitive or off-topic content) to focus her review. Once approved, questions go into the live question bank. Dana can also upload or write her own questions to supplement. The platform tracks source and versioning of questions so that any problematic question can be traced and fixed. Over time, as Dana and others approve more AI-generated content, the question bank becomes both huge and reliable, boasting “thousands of ACT practice questions” for students.

These personas illustrate how each user type benefits from the platform. Their needs drive the requirements for features and design: **students need personalized, engaging practice**; **teachers need efficient class management and insight tools**; **administrators need oversight and compliance**; and **content managers need robust content creation tools with AI assistance**. Next, we detail the features and requirements to meet these needs.

## User Roles and Permissions

To accommodate the different user types, the platform implements a role-based access control system. Each **user role** has specific permissions and a tailored user interface. Below are the key roles in the system and their permissions:

- **Student (Learner):** Can sign up or be invited by a teacher. Permissions include:

  - Take practice quizzes and full-length exams (multiple attempts allowed or as configured by a teacher).
  - View their own study plan, assignments, and progress dashboard.
  - Access explanations and use the AI tutor/chatbot for help on questions.
  - Track personal performance analytics (scores, improvement over time, topic mastery).
  - Customize certain settings (e.g., set target score, receive notifications).
  - **Restrictions:** Cannot view other students’ data, cannot create or edit content, and cannot access administrative settings.

- **Teacher (Instructor/Tutor):** A teacher account may be associated with one or more classes or groups of students.

  - Create and manage **assignments**: select or generate practice questions and exams to assign to students or classes (e.g., schedule a full ACT practice test for the weekend).
  - Personalize study plans for students or approve automatically generated plans.
  - Monitor student progress: access analytics dashboards for each student and aggregate reports for their class. They can see scores, question-wise performance, time on task, etc.
  - Provide feedback: add notes or additional resources to student results, or adjust difficulty settings for a student if needed.
  - Manage their class roster: invite students to the platform, remove students, or move students between classes (if applicable).
  - **Restrictions:** Cannot access system-wide admin settings or other teachers’ classes by default. Typically cannot create new content for the global bank (unless also given content manager privileges), but may be allowed to create custom questions for their class use in some configurations.

- **Content Manager (Content Editor/Curator):** This role focuses on content creation and curation.

  - Generate new content using the AI tools: e.g., prompt the system to create questions, exams, or explanations.
  - Edit and review questions, answers, and explanations in a moderation queue **before** they are published to students.
  - Organize the question bank: tag questions by subject (English, Math, etc.), topic (algebra, punctuation, etc.), difficulty level, and past ACT exam alignment (if replicating real test distributions).
  - Manage a library of study materials: upload or link additional resources (videos, articles, etc.) into the platform’s resource library if provided.
  - **Permissions:** May approve or reject AI-generated content, ensuring quality control. Can also retire or update old questions. Typically only internal staff or authorized educators have this role.
  - **Restrictions:** No access to student personal data or class management (unless the same person also has a teacher role). They operate in the content domain of the platform.

- **Administrator (Org Admin or System Admin):** Two levels of admin may exist:

  - _Organization Admin (School/Tutoring Admin):_ For a specific institution or customer, this admin can manage users within their organization. Permissions:

    - Add or remove teacher accounts, and oversee all student accounts in their organization.
    - Configure organization-wide settings (e.g., school name, logo on the platform if white-labeled, subscription details).
    - View high-level reports aggregating data across all classes (e.g., the average improvement of all students in the school, or usage statistics like total hours practiced).
    - Ensure compliance settings are in place (e.g., ensure all students have consent forms if required, manage data export or deletion requests for their org).
    - Possibly manage integration settings for their org (like linking the platform to their LMS or SSO provider, if not handled by system admin).
    - **Restrictions:** Cannot see content or students from other organizations. Cannot alter the platform’s fundamental configuration.

  - _System Admin (Platform Admin):_ For the platform provider’s internal team. Permissions:

    - Full access to all data and settings across the system (needed for support and maintenance, but used carefully under strict security protocols).
    - Manage global settings (AI model updates, system-wide configurations, maintenance schedules).
    - Monitor system health and usage, manage subscriptions and billing info for all organizational clients.
    - Access all content (can act as super content manager) and all user accounts if needed for support.
    - **Note:** This role is typically not used by end users, only by the company’s support/devops. This is mentioned for completeness of roles but may not be exposed in the UI.

- **Parent/Guardian (optional, if considered):** _If the platform intends to involve parents,_ a read-only role could be given to parents to view their child’s progress and study plan. (This role is optional and would have very limited permissions, primarily viewing certain student reports with the student’s consent.)

**Role Hierarchy and Permissions Summary:** In general, **students** have the least permissions (limited to their own data), **teachers** have more (access to their students’ data and assignment creation), **content managers** have special privileges in the content domain, and **admins** have the broadest control (either within their org or system-wide). The platform should enforce these permissions so that, for example, a student cannot access another student’s results, and a teacher cannot modify content unless authorized, etc. All sensitive actions (like content approval or user management) should be logged for audit purposes. A matrix of roles vs. permissions can be used during implementation to ensure clarity:

| **Role**        | **Key Permissions**                                                                                                    | **Interface Provided**                                                                                |
| --------------- | ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Student         | Take quizzes/tests; view own scores & explanations; follow study plan; use AI tutor chatbot for help.                  | Student Dashboard, Test Interface, Study Plan page, Progress Reports (personal).                      |
| Teacher/Tutor   | Assign content; generate tests; view student and class analytics; manage student list in class; adjust study plans.    | Teacher Dashboard (class overview), Student Performance pages, Assignment Creator, Analytics Reports. |
| Content Manager | Generate/edit questions and exams; approve content; organize question bank; update explanations.                       | Content Management Console (question editor, AI generation tools, content library views).             |
| Org Admin       | Manage users (teachers/students) in org; view aggregate outcomes; configure org settings; handle integrations for org. | Admin Dashboard (org overview), User Management page, Org Settings, Org Reports.                      |
| System Admin    | Full system management; all data access for support; configure global settings and AI models; view overall usage.      | System Admin Panel (all orgs, system health, global config, billing management).                      |

This clear separation of roles ensures that each type of user has access to the features they need and nothing more, supporting security and ease of use.

## Key Features and Functionality

The platform offers a rich set of features to meet the needs of the target users. Below are the **key features**, each critical to fulfilling the platform’s purpose:

### 1. AI-Generated ACT Practice Questions

The platform can automatically generate a wide range of **practice questions** covering all sections of the ACT (English, Math, Reading, Science, and optional Writing prompts). Using an AI model (likely a large language model trained or fine-tuned on educational content), it can produce new questions on demand. Key characteristics:

- **Diverse Question Bank:** The system can generate thousands of unique multiple-choice questions aligned with ACT style and difficulty. This ensures students “never run out of questions” for practice. Questions span all content areas:

  - English: grammar and rhetoric questions (usage/mechanics, organization, style).
  - Math: from algebra, geometry, to basic trigonometry – with varying difficulty. Option to include both calculator and non-calculator practice if relevant.
  - Reading: passages with comprehension questions, including main idea, detail, inference, etc.
  - Science: data interpretation, experiment analysis, scientific reasoning questions.
  - Writing: essay prompts for practice (with sample essays or AI feedback possibly).

- **ACT-aligned Difficulty and Format:** Each question is generated to match ACT format (4 answer choices for multiple-choice, one correct answer). Difficulty is tagged or adjustable – e.g., easy (questions most students get right), medium, hard (questions that differentiate top scorers). The content manager or AI uses **ACT College and Career Readiness Standards** to ensure coverage of skills at various score levels. _For example, math questions might be generated with content spanning pre-algebra through precalculus to mimic the ACT’s distribution._ The AI references these standards to ensure relevance (e.g., focusing on skills ACT expects).
- **Quality Control via Human-in-the-Loop:** AI generates the questions, but a content manager can review them (especially initially) to ensure they are free of errors and properly formatted. The platform may also use automated checks (for instance, verifying that exactly one answer is marked correct and others are plausible distractors, checking that the reading passage questions reference the passage correctly, etc.). All AI-generated questions, answers, and explanations go through a review process to be **“reviewed and verified” by experts before release**. This prevents issues where the AI might inadvertently produce inaccurate or confusing content.
- **Regeneration and Feedback:** If users (teachers or students) find an issue with a question (e.g., a flawed question or ambiguous answer), they can flag it. The system logs such feedback for content managers to review and improve. The AI could even suggest a fixed version. This creates a continuous improvement loop for the question bank.
- **Example Usage:** A teacher could click “Generate 10 new Science questions about experimental design” and the AI will produce those questions on the fly, which the teacher can assign immediately if they trust the quality (or after a quick review). Students using practice mode will be served questions from this rich bank appropriate to their level (see Adaptive Practice below).

### 2. AI-Generated Full-Length ACT Exams

Beyond individual questions, the platform can compile **full-length practice tests** that mirror the actual ACT exam structure. This includes an **English section (75 questions, 45 minutes)**, **Math section (60 questions, 60 minutes)**, **Reading section (40 questions, 35 minutes)**, **Science section (40 questions, 35 minutes)**, and optionally a **Writing essay (40 minutes)**. Features of this component:

- **Realistic Test Simulation:** The exams generated use the same timing, number of questions, and section order as the official ACT. They are assembled to match the content distribution and difficulty of real ACT tests. For example, the English section will include a balance of grammar topics, Reading will have 4 passages (fiction, humanities, social science, natural science genres), etc. This gives students the **experience of a full ACT in practice** so they are comfortable on test day.
- **AI Assembly and Randomization:** The platform can randomly generate or select questions from the bank to create unique tests each time. Alternatively, it might have a set of pre-generated full tests that are saved for consistency (e.g., 10 practice tests similar to official ones). Each test generation ensures that the overall difficulty is balanced – for instance, not all hardest questions end up in one test. The AI might even consider prior tests a student has taken to avoid repeat questions or to purposely include previously missed questions as needed.
- **Diagnostic Test Mode:** One recommended approach is to have a **Diagnostic Test** as the first full-length exam a student takes. This initial test assesses the student’s baseline score and subscore strengths/weaknesses. The platform uses this diagnostic to generate a **personalized study plan** (feature 3 below). The diagnostic can be an AI-generated test or a standard test from previous ACT exams for accuracy. Either way, it is delivered within the platform and scored immediately.
- **Test-Taking Interface:** (More in UI section, but worth noting here) The platform’s test interface includes features to simulate test conditions:

  - Timers for each section (with optional accommodations like extended time if configured for certain students).
  - Ability to **mark questions for review**, skip and come back within a section.
  - Option to eliminate choices (just as a student might cross out options on paper) – e.g., click to strike through an option.
  - A **pause** feature for practice mode (if a student cannot finish in one sitting, though in a strict exam simulation this might be disabled).
  - **Auto-scoring** at the end, providing an estimated ACT score for each section and composite.
  - **Projected Score** feature: after each full test, the platform shows the student’s estimated ACT score (e.g. “Composite 28”) so they know where they stand.

- **Multiple Test Forms:** The system might come with a set number of full tests (e.g., 5 or 10) that are well-vetted. After those are used, it can generate additional ones or recombine questions so students have virtually unlimited practice. Teachers can choose to assign a specific test form or let the system pick one at random for each student.
- **Analysis of Results:** Immediately after a student completes a full-length test, they receive a detailed breakdown (and so does their teacher). This includes section scores and possibly subscores or skill metrics (e.g., in Math, how they did on algebra vs geometry questions). It also provides the correct answers and the student’s answers, with the option to review explanations (which ties into feature 4).
- **Simulation of Test Conditions:** The platform could optionally restrict certain aids during a simulated test – for example, in a full test mode, the AI hints/explanations might be turned **off** until after submission, to mimic real exam conditions. In a practice mode, those hints can be available question by question.

### 3. Personalized Study Plan Generation

One of the standout features is the creation of a **personalized study plan** for each student, using AI to tailor the plan based on the student’s performance, target test date, and goals.

- **Initial Plan from Diagnostic:** After a student takes a diagnostic test (or inputs a baseline score), the platform generates a recommended study schedule. This plan covers the time until the student’s ACT test date (which the student can input) or a default period (e.g., a 3-month plan). It breaks down study sessions by week (or even by day) specifying what the student should focus on. For example:

  - Week 1: Focus on English grammar (commas, punctuation rules) and Algebra basics. Complete 50 practice questions in these areas, do 1 reading passage every other day to build speed.
  - Week 2: Focus on coordinate geometry and science reasoning. Take one full-length practice test at end of week.
  - etc., up to the test date.

- **Adaptive and Dynamic:** The study plan is not static. As the student progresses, the plan adapts. If the student is ahead of schedule or has mastered a topic early, the AI might introduce new goals or more advanced topics. Conversely, if the student is struggling in a planned area (say the plan had them improving in Science by now but their performance still lags), the plan will adjust to allocate more time to Science. This **adaptive scheduling** ensures the plan stays relevant.
- **Customization and Overrides:** Students and teachers can adjust the plan. The student might indicate they can study more hours per week or need to take a break during holidays – the plan can accommodate these inputs. Teachers can also fine-tune the plan for their students, for instance, adding an assignment (“Teacher wants you to write 2 essays this month”) or modifying the focus if they know the class will cover some topics offline.
- **Reminders and Checklists:** The platform provides a **checklist or calendar view** of the study plan. Each item (study session, quiz, test) can be checked off when done. Automated reminders or notifications (email/SMS/app notifications) can prompt the student about upcoming tasks (“Reminder: Complete 3 reading passages this week as per your study plan”). This keeps students accountable and on track.
- **AI Assistance in Planning:** The AI considers various factors when generating the plan:

  - **Target Score:** If a student’s goal is a 30 and their diagnostic was 24, the plan will be more intensive than for someone aiming for a 26 from a 24.
  - **Strengths/Weaknesses:** Emphasize weak areas but also ensure strengths are maintained. For instance, if a student is strong in Math but weak in English, plan might allocate more English practice but still include some math to keep it sharp.
  - **Available Time:** Number of weeks to test, hours per week student can commit (maybe asked via a quick survey).
  - **Learning Preferences:** If known, e.g., some students prefer doing a full test every week, others prefer shorter daily practice. The plan could be adjusted accordingly (with teacher input).

- **Integration with Calendar:** The study plan could be exportable to external calendars (Google Calendar, etc.), so students can see their study tasks alongside their other events. Integration with calendar also allows scheduling of any live sessions if that’s in scope (like teacher-led sessions or classes).
- **Progress Monitoring:** The study plan ties into progress tracking – as the student completes tasks, the platform marks them done and can visually show progress through the plan (like a progress bar or timeline). If the student falls behind (tasks overdue), it can gently prompt them or adjust by rescheduling pending tasks into the remaining time.
- **Example:** Alex (student persona) after diagnostic gets a plan that every week has: 3 days of short practice (20-minute sessions focusing on weak areas), 1 day of rest or light review, and every Saturday a longer session or a section test. As Alex practices, the plan marks off tasks and shifts focus according to what Alex is getting wrong (more emphasis on Reading if he continues to struggle there, for instance).

### 4. Detailed Answer Explanations and AI Tutor Assistance

A critical learning feature is that for every practice question or test, the platform provides **detailed explanations** for the correct answer and the incorrect options. Additionally, an **AI tutor chatbot** is available to give hints or answer follow-up questions in real time.

- **Explanation Generation:** For each question (whether AI-generated or entered by content creators), the system either generates or stores a step-by-step explanation. These explanations aim to teach the concept needed. For example, a math question’s explanation will show how to solve it algebraically, and perhaps mention common mistakes (like if a wrong choice corresponds to a typical error). For reading or science, the explanation might point out which part of the passage or data leads to the correct answer. The AI can generate these, and content managers review them for accuracy and pedagogy.
- **In-Depth Hints:** Instead of immediately revealing the full explanation, the platform can give **hints** to students who are stuck. The AI tutor can provide progressive hints: the first hint might be general (“Recall the rule for comma usage in this context…”), the second hint more specific (“Look at the underlined portion, is it an independent clause?”), and finally the student can request the full explanation. This mimics how a human tutor might help a student figure out an answer with guidance rather than just telling them outright. Students can ask for hints during practice mode on any question. (During a timed test mode, hints might be disabled to simulate real conditions).
- **AI Tutor Chatbot:** The platform features a conversational AI assistant integrated into the study interface. Students can **ask questions in natural language** about anything related to the ACT prep:

  - They might ask “Why is the answer B? I thought C was correct because...?” and the AI, knowing the context of the question, can clarify the difference between B and C, referring to the explanation.
  - They could ask broader conceptual questions like “Can you explain the difference between its and it’s?” or “How do I approach science passages faster?” The AI draws on a knowledge base of grammar rules, math formulas, and test-taking strategies to respond.
  - The chatbot is available 24/7, essentially acting as an on-demand tutor. It is context-aware when invoked from a question (so it knows what the question is and what the correct answer is), but it can also answer general ACT questions if asked outside of a specific problem.

- **Follow-up Q\&A:** Importantly, students can ask **follow-up questions** if they don’t understand the explanation. For example, “I still don’t get how you solved for x in step 2, can you elaborate?” The AI will then break it down further. This interactive explanation helps ensure the student truly learns the concept, not just memorizes the answer.
- **Quality and Tone:** The explanations and AI tutor are crafted to be **clear, concise, and encouraging**. The language is student-friendly, avoiding overly technical jargon unless needed. If the student asks something outside the AI’s scope (like unrelated questions), the AI politely steers back to ACT prep. All content from the AI tutor should be monitored to avoid any inappropriate or misleading responses (the AI model should have a content filter given the audience is minors in some cases, and domain-limited to ACT topics).
- **Use Case Example:** A student practicing a math question gets it wrong. The result page for that question shows: the correct answer is X, and a “Show Explanation” button. The student clicks it to read the step-by-step solution. Still confused at step 3 of the solution, the student clicks “Ask AI Tutor” and types a question asking for clarification. The AI Tutor responds with a different explanation approach or further detail. The student gains understanding and moves on. If the student had been completely unsure how to start, they could have clicked “Hint” while doing the question, which might have said “Try plugging the answer choices to see which satisfies the equation” – a nudge without giving it away.

### 5. Adaptive Practice and Adaptive Difficulty

To maximize effectiveness, the platform implements **adaptive learning** mechanisms. This means the difficulty and selection of questions dynamically adjust to the student’s performance level, providing a personalized challenge:

- **Adaptive Question Selection:** When a student is in practice mode (not taking a fixed test), the system selects questions based on their past performance. For instance:

  - If a student has been answering medium-difficulty algebra questions correctly, the system might start showing them harder algebra questions to stretch their skills.
  - If a student is struggling with reading inference questions, the system will present more of those (at an appropriate level) to help them practice that specific skill.

- **Difficulty Levels:** Each question in the bank is tagged or internally rated by the AI with a difficulty metric. The platform might use a simple 3-tier (easy, medium, hard) or a more granular scale (e.g., 1-5). Initially, the student might get a mix or start around medium. As the student answers:

  - Consecutive correct answers -> slight increase in difficulty of subsequent questions.
  - Consecutive incorrect answers -> slight decrease to rebuild confidence and address fundamentals.
    This ensures the student is usually operating in their “zone of proximal development” – not bored by too-easy questions, but also not frustrated by too-hard ones.

- **Topic Adaptivity:** The adaptivity also considers content areas:

  - If a student consistently does well in Math but poorly in English, the system may allocate more practice time or questions to English.
  - It can detect specific subtopics: e.g., a pattern of missing probability questions in Math triggers more practice in probability.

- **Periodic Reassessment:** The adaptive algorithm might occasionally throw in questions of varied difficulty to gauge progress. For example, even if a student is at “hard” level in Math, an easy question might appear occasionally to ensure they have basic skills solid (and provide a confidence boost). Or a very hard question might be given to test the upper limits of the student’s ability. These also help avoid the student gaming the system by intentionally getting some wrong to avoid hard questions – the system continually probes.
- **Adaptive Full Tests:** While full-length tests are typically fixed forms, the platform could offer an **adaptive testing mode** (like how the GRE is adaptive). An adaptive ACT might not be standard, but as a practice tool, we could allow an adaptive exam where the question difficulty adapts within each section based on responses. This can produce a more efficient test (fewer questions needed to estimate ability). However, since ACT is linear, this might be an optional feature or future possibility.
- **Mastery Learning Path:** The ultimate goal of adaptivity is to guide the student along a learning path. The platform can have a concept of **mastery levels** for each skill. As the student answers questions correctly, the system marks those skills as improving and introduces new or higher-level skills. If mistakes occur, it may drop back to review easier items on that skill.
- **Transparency and Control:** The adaptive system should be somewhat transparent to teachers (and maybe students). For example, a teacher could see that “the system has identified John at a 70% mastery in Algebra II concepts and is giving him harder problems in that area.” If needed, teachers can override or adjust (for instance, “I want John to focus on moderate difficulty for now despite the system thinking he’s ready for hard, because I want him to gain confidence”). There might be a setting to turn off adaptivity for certain assignments (e.g., a teacher can assign a fixed difficulty set).
- **Benefits:** Adaptive difficulty helps keep students engaged and challenged appropriately. It also accelerates improvement by targeting weaknesses without over-practicing strengths. Students who are behind get remedial questions to build up, while advanced students are pushed to reach their maximum potential (e.g., those aiming for a top score 35-36 will get the toughest questions).
- **Example Scenario:** Beth the tutor runs an adaptive practice session for her class. Student A (stronger student) is quickly funneled to difficult questions because she keeps getting them right – eventually dealing with very challenging ACT problems that push her towards a 34-36 range. Student B (weaker) after a few mistakes is given easier, instructional questions that include more scaffolding in the explanations. Each student ends the session having practiced the most appropriate set of questions for them. Both students felt challenged but not overwhelmed.

### 6. Analytics Dashboard and Performance Tracking

The platform provides robust **analytics dashboards** for students, teachers, and admins to track performance and progress over time. Data-driven insights are at the core of demonstrating improvement and guiding further study.

- **Student Dashboard (Analytics for Students):** When a student logs in, their homepage is a snapshot of their current progress:

  - **Score Tracking:** If the student has taken multiple full-length practice tests, it shows a graph of their composite score progression over time (e.g., a line chart from Diagnostic 24 to latest practice 28). Section scores might also be shown.
  - **Topic Mastery:** A breakdown of performance by subject and subtopic. For example, “Math: 80% correct overall – Algebra 90%, Geometry 70%, Trig 50%” etc., often visualized with bar charts or proficiency meters. This helps the student see where they need to improve.
  - **Recent Activity:** Summary of what the student did recently – e.g., “Completed 30 questions in Science yesterday with 70% accuracy, mostly in Data Representation type.” It might highlight achievements (“5-day practice streak!”) to motivate.
  - **Upcoming Plan:** A quick view of what’s next in their study plan (like “This week’s goal: Complete Full Test #3 and review Geometry mistakes”).
  - Possibly a **comparison** to target: e.g., “Your goal score: 30, you’re 2 points away in English, 4 away in Math,” etc.

- **Teacher Dashboard (Analytics for Teachers):** Teachers get a multi-student view:

  - **Class Overview:** For each class or group, a dashboard shows average scores, distribution of scores (e.g., how many students in the 20-24 range, 25-29 range, etc.), and class progress towards goals.
  - **Student List with Key Metrics:** A table or list of students with columns like latest score, improvement since start, number of practice tests taken, completion of assigned tasks (%) and perhaps a “risk flag” if a student is falling behind or not practicing enough.
  - **Drill-down Analytics:** Clicking on a student brings up that student’s detailed analytics (similar to student’s own view but with maybe additional info for teacher like comparison to class average). Teachers can also filter analytics by topic: e.g., see the class accuracy in each subtopic to identify commonly weak areas (maybe the whole class is weak in Science/data interpretation – teacher then knows to review that in class).
  - **Custom Reports:** Teachers can generate reports for parent-teacher meetings or student feedback sessions. For instance, a PDF report of a student’s progress over 8 weeks, highlighting strengths, weaknesses, and recommended focus going forward.
  - **Time Analytics:** See how much time each student spends on the platform (useful to correlate effort with improvement).

- **Admin Analytics (for School or Org Admin):**

  - **Organization Summary:** How many students are actively using the platform, average improvement, distribution of scores across the school.
  - **Teacher Performance Metrics:** Possibly see which classes or teachers’ students have the highest gains, or identify usage patterns (maybe some teachers not utilizing the platform fully – admin can encourage more use).
  - **Content Usage:** Stats on question bank usage – e.g., which subjects/questions are most attempted, which questions have high error rates (could indicate either those questions are good differentiators or possibly flawed).
  - **License Utilization:** If a school purchased 100 licenses, see how many are in use, etc.

- **Data Visualization:** The dashboards use clear charts and graphs for quick understanding. They might use color-coding (red/yellow/green) to indicate performance levels. For example, topics where a student is below a certain threshold could be marked in red as “Needs Improvement.”
- **Progress Over Time:** A key aspect is showing progress, not just static scores. Graphs or timelines that show improvement (or stagnation) help motivate students and inform teachers. E.g., “You have improved by 5 points in Math since last month” or “Your English score has plateaued, let’s focus there.”
- **Benchmarking:** The platform could include benchmarks like ACT College Readiness Benchmarks or percentile rankings. For instance, show students how their practice score might translate to a percentile nationally. Or an admin might see how their school’s average compares to a national average (if data is available or if the company aggregates anonymized data across all users).
- **Export and Share:** The analytics can be exported (PDF reports for parents, CSV data for further analysis). A teacher might export a spreadsheet of all question responses for their class if they want to do item analysis.
- **Real-Time and Historical Data:** After each test or practice session, data is updated in real-time. The system also stores historical data so one can look back at, say, Q1 vs Q2 performance or pre- and post- a winter bootcamp.
- **Alerts and Insights:** The analytics engine might proactively alert users of notable insights:

  - Students: “You consistently score 10% higher on Math questions when you do them in the morning vs late at night” (if such patterns can be detected), or “You have mastered medium-level Algebra – try more difficult ones.”
  - Teachers: “None of your students have practiced Reading in the last week” or “Student X’s performance has dropped in the last two tests, possibly indicating burnout or a concept gap.”
  - These are nice-to-have intelligent insights that AI could glean from the data to further help.

- **Examples:** Carlos (admin persona) could pull up a dashboard showing that across the 100 students in the program, average composite has risen from 22 to 25 in 3 months, with biggest gains in Math. He also sees maybe a particular teacher’s class has lower usage – prompting him to check in. Meanwhile, Beth (teacher persona) looks at her class dashboard and quickly spots that Science section scores are lagging, so she decides to do a special session on Science reasoning next week. A student, Alex, checks his dashboard to see he’s now consistently in the 30s for English (green check mark next to English), but his Science is still in the low 20s (red exclamation icon), reinforcing that he should spend extra time on science as his study plan suggests.

### 7. Progress Tracking and Performance Feedback

While analytics provide the data, **progress tracking** is about making that data meaningful as feedback to the learner. This feature overlaps with analytics but is focused on the **individual’s learning journey**:

- **Progress Milestones:** The platform can set milestones or goals for students and then track them. For example, milestones like “Score 25 on next practice test” or “Complete 100 practice questions in Math”. When milestones are achieved, the platform can congratulate the student (badges, achievement unlocks, or simple messages).
- **Streaks and Consistency:** To encourage regular practice, it tracks streaks (e.g., days in a row of study, or weeks in a row hitting a goal of hours studied). It might show “You have a 10-day streak!” or “You practiced 4 out of 5 days this week.” Such gamified elements can motivate students.
- **Adaptive Goals:** If a student surpasses a goal easily, the system can set a new higher goal (with teacher approval possibly). If they struggle, it can set intermediate smaller goals to keep them motivated.
- **Review of Mistakes:** Progress tracking includes tracking _learning progress_, not just scores. The platform keeps a record of questions the student got wrong and whether they have since gotten similar questions right. A feature often called “**Practice your mistakes**” allows students to review all questions they answered incorrectly in the past. They can retry these or get additional similar questions until they get it right. This ensures they close knowledge gaps.
- **Competency Mastery Indicators:** The system can show a “mastery” level for each skill or subject (e.g., a progress bar that fills up as the student answers more questions correctly for that skill). Mastery could be defined (for example, 5 consecutive correct answers on hard questions on a topic might mark it as “Mastered”).
- **Regular Feedback Messages:** The platform gives narrative feedback to the student, akin to what a coach would say:

  - E.g., “Great job! You improved your Reading score by 3 points since last test. Your efforts in timing yourself on passages are paying off.”
  - “You seem to struggle with Geometry questions involving circles. We recommend reviewing circle theorems. We’ve added a short lesson in your study plan.”
  - These messages can be auto-generated based on rules (score changes, category performance) and make the experience more personalized.

- **Teacher Feedback Integration:** Teachers can add their own comments on student progress reports. For instance, after a student takes a test, the teacher might write a quick note in the system that the student will see: “Keep it up on English, but double down on vocab for Reading – try the flashcards I assigned.”
- **Visualization of Progress:** In addition to dashboards, a simpler progress chart or even a **timeline** of achievements might be presented to students. For example: “Week 1: Diagnostic 22; Week 4: Practice Test 1 = 24; Week 8: Practice Test 2 = 26; Goal: 28 by Week 12” displayed as a timeline or ladder.
- **Parent Reports:** If parents are involved or want updates, the system can produce a parent-friendly progress email or report periodically (highlighting improvement and next steps, without overwhelming with data).
- **Encouragement and Gamification:** Earning points or badges for completing tasks (like a badge for completing first full test, or for logging in every day for a week) can be part of progress tracking. A leaderboard could be optional (e.g., within a class, if considered healthy competition, showing top practice question solvers) – but use with care as it might discourage some; likely a minor feature if any.
- **Retention of History:** All prior attempts, scores, etc., are saved so a student at any time can look back and see how far they’ve come. This historical record is crucial for reflective learning and also for any external analysis (like if the platform wants to analyze efficacy across many students).
- **Outcome Tracking:** Ultimately, progress tracking would tie into whether the student hits their target ACT score (if they report their actual test score back or if they take an official test via the platform for state testing etc.). That final outcome can be recorded to measure success of the prep.

By combining analytics and progress tracking, the platform not only provides data but also uses it to guide and motivate students continuously, making the learning experience targeted and encouraging.

### 8. User Interface & Experience (UI/UX) Highlights

_(Note: A more detailed UI/UX requirement with wireframes is in a later section. Here we list key features relevant to the product’s capabilities.)_

The platform’s user interface is modern, intuitive, and responsive, ensuring ease of use across devices (desktop, tablet, mobile). Key UI/UX features include:

- **Dashboard Interfaces:** Clear dashboards for each user type as described, using visualizations to communicate progress. Navigation from the dashboard to detailed views is logical (e.g., clicking a metric drills down into that metric’s details).
- **Responsive Design:** Students can use the platform on a computer web browser or on a mobile device (either via responsive web or a dedicated mobile app). Studying on-the-go is supported. Timed full tests might be recommended on a computer, but practice questions and review can be done on mobile conveniently.
- **Accessibility:** The design follows accessibility standards (contrast, screen reader support, keyboard navigation) so that all students, including those with disabilities, can use the platform. For example, screen-reader friendly labels for all content, ability to increase font size, etc.
- **Localization (if needed):** While the ACT is primarily in English, the UI could support multiple languages for instructions if expanding to international markets (so the navigation and help could be in Spanish, etc., though content remains English).
- **Consistency:** A unified look and feel with the organization’s branding (if white-labeled for a school, perhaps allow them to add logo). Buttons and menus behave consistently throughout.
- **Feedback and Responsiveness:** The UI provides immediate feedback on actions. E.g., when submitting a test, a loading indicator shows scoring in progress, then results appear. When the AI tutor is asked a question, it shows a “...thinking” animation before the answer.
- **Error Handling:** User-friendly messages if something goes wrong (e.g., “We’re having trouble generating that question, please try again” if the AI fails to produce content within a timeout).
- **Secure Login and Onboarding Flows:** New users have a simple onboarding, possibly with a tutorial highlighting features. Multi-factor auth can be enabled for security on accounts.
- **Personalization:** Users can set preferences (dark mode for studying at night, notification preferences, etc.). The platform greets them by name and occasionally might show personalized encouragement (“Welcome back, Alex! Ready to beat yesterday’s score?”).

The UI/UX is not just aesthetic; it’s pivotal for engagement, especially for teens who may have short attention spans or be intimidated by test prep. A friendly, game-like and interactive interface can make studying less of a chore and more of a guided journey.

_(Additional UI/UX specifics and wireframes are in the "Wireframes and UI Design" section.)_

### 9. Integration with External Systems

Integration capabilities are a key feature, enabling the platform to fit into broader educational technology ecosystems:

- **Learning Management System (LMS) Integration:** The platform supports integration with popular LMSs used by schools (such as Canvas, Schoology, Blackboard, Google Classroom, etc.). This could be via **LTI (Learning Tools Interoperability)** standards or specific APIs:

  - Single Sign-On from the LMS: Students and teachers can launch the ACT Prep Platform from within their LMS without a separate login. The LMS passes authentication info (and class roster info) to our platform, streamlining access.
  - Gradebook Sync (if applicable): If teachers want, the results from practice tests or assignments on the platform can be sent back to the LMS gradebook automatically (particularly useful for school teachers who might give a grade for completion or use practice test scores as part of class grading).
  - Class Setup: The platform could import class lists from the LMS, so teachers don’t have to invite students manually – it picks up who’s in the class in the LMS and creates accounts or ties them to that class in our platform.

- **Authentication Providers:** In addition to or as part of LMS integration, the platform supports OAuth/SAML logins:

  - **Google login:** Many schools provide Google accounts, so students/teachers can log in with Google credentials.
  - **Microsoft 365/Azure AD:** Similarly, support Microsoft accounts or any SAML identity provider the school uses (for enterprise single sign-on).
  - **Social Logins for individual users:** If individual students (not through school) use the platform, they might log in with Google, Facebook, etc., or just email/password.

- **Calendar Integration:** Integration with external calendar apps (Google Calendar, Outlook) to push study plan schedule or reminders. E.g., the platform can create calendar events for “ACT Practice Test at 10am Saturday” for the student.
- **Communication Tools:** Possibly integrate with email or messaging for notifications. For instance, email integration to send summary reports to students weekly, or an integration with SMS/WhatsApp API for reminders if opted-in.
- **Content Integration:** The platform might integrate with content repositories or resources:

  - If there are popular flashcard apps or tools, integrate to send vocabulary lists or math formula flashcards relevant to ACT.
  - Or link with video content libraries (like YouTube, Khan Academy) for explanatory videos: e.g., after an explanation, link to a Khan Academy video on that concept if more help is needed.

- **Reporting and Data Export:** Integration for data analysis: for advanced schools or researchers, allow exporting data to systems like Excel, or directly to Google Sheets. Possibly provide an API for administrators to pull raw data (scores, usage logs) into their district’s data warehouse.
- **Payment and CRM Integration:** (For the business side) The SaaS platform might integrate with payment gateways (for subscription handling if sold directly to students or schools). Also integration with CRM (like Salesforce) for sales/account management if relevant, but that’s more internal.
- **Third-party AI Services:** If using external AI (like OpenAI’s API for content generation), the platform integrates via API calls to those services. This is internal integration but crucial – ensuring if one AI service fails or becomes too costly, the architecture allows swapping to another (perhaps fine-tuned local model) seamlessly.
- **Plagiarism or Cheating Prevention Tools:** Possibly integrate with proctoring services or plagiarism checkers for the essay portion (to ensure a student’s essay is original or to simulate the scoring process).
- **Browser/Device Integration:** If needed, an offline mode or an app that can let students download some practice to do offline (for those with limited internet) and sync later.

Through these integrations, the platform is not a silo but part of the larger educational workflow, making adoption easier and adding value by connecting with tools teachers and students already use.

### 10. Security and Data Privacy Features

_(Though security and privacy are also in Non-functional Requirements, here we highlight user-facing or functional aspects related to them.)_

- **Secure Data Handling:** All user data (personal information, scores, etc.) is stored securely (encrypted in transit and at rest). Users can trust that their data is protected.
- **Privacy Controls:** The platform provides clear privacy settings and consent forms. For instance, if a student is under 13 (though rare for ACT age, but possible in cases of very early test-takers), parental consent via COPPA compliance flows is required. Students (or their guardians) might have control over what data is shared with teachers or others. For example, a student in a self-study mode not tied to a class might choose not to share their data publicly.
- **Compliance Features:** The platform adheres to **FERPA** regulations for educational records – meaning a student’s scores and records are only accessible to authorized users (the student, their teacher, school officials with legitimate educational interest). If a student leaves the school, their data can be transferred or deleted per policy. The system allows data export for schools that need to maintain local records.
- **Account Security:** Multi-factor authentication is available for admin and teacher accounts (and optional for students). Passwords are hashed, and login attempts are monitored for abuse.
- **Role-based Access in UI:** As noted, students cannot see other students; teachers only see their students; content managers only access content section, etc. This is enforced at the UI and API level.
- **Audit Logs:** Important actions (like content approvals, admin changes, score overrides) are logged. If there’s a need to audit who did what (critical for both security and when resolving any disputes or issues), the logs provide a trail.
- **Session Management:** Automatic logout after periods of inactivity (especially on shared computers at school) to prevent someone else using a logged-in account.
- **Backup and Recovery:** While not user-facing, it’s worth noting the system keeps backups of data so nothing is lost (if a student accidentally deletes their account or something, administrators can recover data within a grace period).
- **Data Retention Policy:** Students and admins are informed how long data is kept. For example, practice data might be kept for X years. If needed, tools for students to delete their account/data (especially under GDPR for EU users).
- **CIPA compliance:** If used in K-12 schools, ensure any open communication (like the AI chatbot) is safe — e.g., it won’t allow sharing of personal info and doesn’t expose the student to external content outside of the educational scope, aligning with CIPA (Children’s Internet Protection Act) which schools follow for safe internet usage.
- **No PII in AI:** If using AI services, ensure that we’re not sending sensitive PII through external AI API calls (or have agreements in place), preserving student anonymity as needed.

All these features build trust with schools and users that the platform is safe to use and respects their privacy.

With these key features outlined, the next sections will detail the specific functional requirements, technical implementation considerations, and other aspects needed to make these features a reality.

## Functional Requirements

This section translates the key features into specific functional requirements and user stories, detailing what the system **should do**. It is organized by major functional areas of the platform: Content Creation, Practice & Test-taking, Study Planning, Analytics & Reporting, User Management, etc. Each requirement is described in terms of functionality and acceptance criteria.

### A. Content Creation and Management

This covers how content (questions, exams, explanations, study materials) is generated, stored, and managed.

1. **AI Question Generation**

   - **Requirement:** The system shall enable generation of ACT-style questions using AI, given certain input parameters. For example, a content manager or teacher can specify subject (e.g. Math), topic (e.g. Algebra), and difficulty, and the system returns a set of new multiple-choice questions with correct answer and solution explanation.
   - **Acceptance Criteria:**

     - Users with permission (Content Manager or Teacher if allowed) can input parameters and trigger generation.
     - The system produces a question stem, 4 answer choices (A-D), and marks the correct answer.
     - An explanation for the correct answer is also generated.
     - Generated content is saved as “draft” until reviewed. If auto-approval is allowed (perhaps for quick use by teacher), it’s marked as such with a warning if unreviewed.
     - If the AI cannot generate a question (times out or error), the user is notified and perhaps given an option to retry or slightly change parameters.
     - Quality measures: e.g., no duplicate question exactly like ones in the bank (system should check similarity to avoid repeats).

2. **Question Bank Storage & Retrieval**

   - **Requirement:** The system shall maintain a database of all practice questions (both AI-generated and any imported/handwritten questions), with metadata. It should support efficient retrieval by topic, difficulty, etc., for use in quizzes and tests.
   - **Acceptance Criteria:**

     - Each question record includes: unique ID, subject, topic tags, difficulty level, the question text, options, correct answer, explanation, source (AI generated or manual), and last updated timestamp.
     - The system can fetch questions by criteria (e.g., “give 10 random Science questions of hard difficulty on Data Representation”).
     - Questions can be flagged as active or retired (retired ones won’t be used for new assignments but might remain in reports if attempted historically).
     - Content managers can edit any question in the bank (fix wording, change difficulty tag, etc.). Edits create a new version or audit trail.

3. **Full-Length Test Assembly**

   - **Requirement:** The system shall create full-length tests either from a static set or dynamically. It must ensure the correct number of questions per section and an overall balance.
   - **Acceptance Criteria:**

     - The platform can generate a test upon request with 4 sections (English, Math, Reading, Science) plus optional Writing.
     - Each section’s questions are pulled according to the ACT blueprint: e.g., English gets 75 questions, with roughly the correct distribution of rhetoric/grammar topics; Math 60 (mix of algebra, geometry, etc.), etc.
     - If using a fixed set of pre-defined tests (say Test 1, Test 2, etc.), the system stores those configurations and delivers them consistently.
     - Tests have unique IDs and can be versioned.
     - A generated test can be previewed by a teacher/admin before assigning to ensure quality (especially if dynamically generated).
     - After generation, the test is stored so that all students who take “Test 3” get the same questions (for fairness in a classroom assignment scenario). Alternatively, if each student gets a random test when they click “take a practice test,” that’s allowed for self-practice mode.

4. **Study Material and Resources Management**

   - **Requirement:** The system shall allow adding supplementary study materials (like lessons, strategy guides, video links, etc.) and associating them with parts of the study plan or as references after questions.
   - **Acceptance Criteria:**

     - Content managers can upload or link resources (PDF guides, external URLs, video embeds) into a Resource Library in the platform. Each resource can be tagged by topic.
     - The study plan generator can reference these resources. For example, if a student is weak in “comma usage,” the plan might list a resource “Grammar Guide on Commas” that the student can click to read/watch.
     - After a question is answered incorrectly, the explanation might have a “Learn More” link that goes to a relevant resource in the library.
     - Teachers can add custom tips or resource links to assignments (like “Review Chapter 3 of textbook, link: ...”).
     - All users have appropriate access: students see resources assigned or in a general library; teachers can see/add for their students; content managers see all and manage them.

5. **Content Review Workflow**

   - **Requirement:** The platform shall provide a workflow for reviewing and approving AI-generated content before it is widely used.
   - **Acceptance Criteria:**

     - When AI generates new content, it is marked as “Needs Review” in the content management interface.
     - Content managers get a notification or see a queue of items to review.
     - For each item, they can edit the question text, answers, or explanation. They can test-solve the question and mark it correct.
     - They then set status to “Approved” which allows the question to be used in general circulation for students.
     - If “Rejected,” the question is not used (could be stored for further analysis to improve AI, but not visible to normal users). Possibly allow a reason to be logged.
     - A metric like “AI Generation Quality” can be tracked (e.g., what percentage of generated questions are approved vs need editing vs rejected). This might tie into KPIs for the content team.
     - Admin override: A system admin can bypass or adjust this workflow, e.g. enabling auto-approval for a trusted context.

6. **Manual Content Creation & Import**

   - **Requirement:** Users (with permission) can manually add questions or import them in bulk (for example, if a school has its own item bank or wants to incorporate released official ACT questions under license).
   - **Acceptance Criteria:**

     - An interface for manually adding a question: input fields for question text, answer choices, correct answer, explanation, tags.
     - Ability to import via a spreadsheet or other format for multiple questions at once, mapping columns to those fields.
     - Imported questions also appear in the question bank with appropriate metadata.
     - Manual additions skip AI generation but might still go through a review (maybe auto-approved if a human wrote it, but a content manager could still verify formatting).
     - The system prevents exact duplicates if trying to import something already existing (could warn and skip those).

7. **Content Tagging and Categorization**

   - **Requirement:** Every piece of content (question or test) should be categorized by relevant attributes to enable search and adaptive features.
   - **Acceptance Criteria:**

     - Tags include: Subject (English/Math/Reading/Science/Writing), Specific Skill (e.g., “Geometry – Circles”, or “Science – Conflicting Viewpoints”), Difficulty (Easy/Med/Hard or numeric), ACT Section (for mapping to the test sections).
     - Possibly tag by _ACT College Readiness Standard_ code if mapping to that framework, which can show alignment to those standards.
     - The system can filter questions by any combination of tags for assignment or analysis.
     - Adaptivity logic uses these tags to know what category a student is weak in (if many questions tagged “Geometry – Circles” are wrong, it knows that category needs work).
     - Content managers can adjust tags if needed (especially for AI-generated questions where initial tagging might be AI-driven and could err).

### B. Practice and Test-Taking Functionality

This covers the end-to-end process of a student taking practice questions or exams, and the immediate feedback loop.

1. **Quiz/Practice Mode Session**

   - **Requirement:** Students can engage in an open-ended practice session focusing on a particular subject or mixed subjects, with or without time constraints, with adaptive difficulty enabled.
   - **Acceptance Criteria:**

     - Student can choose a practice mode session from their dashboard (options might include: “Adaptive practice” which automatically serves questions, or “Custom practice” where they select subject/topics and number of questions).
     - The session starts presenting questions one at a time. The student answers each and gets immediate feedback if configured (could be a toggle “Practice with immediate feedback” vs “Practice without seeing answers until the end”).
     - If immediate feedback is on: right after answering, the system shows whether correct or not, plus explanation and an option to ask the AI tutor more if needed. The student can then proceed to next question.
     - If immediate feedback is off: the system simply records the answer and moves to next question, and at the end of the session a summary is shown with what was right/wrong.
     - The student can quit a practice session anytime, and the system will still record what was done up to that point. If they quit early, it should note maybe “15 out of 20 questions completed” in their log.
     - Adaptive difficulty in effect (if enabled in settings): as described, adjusting question picks based on performance in that session and overall history.
     - The student can access hints during practice: e.g., a “Hint” button that provides a hint (possibly at some cost like reduced points in a gamification context, but since it’s practice, likely just freely). Too many hints used could be logged for the student to reflect on.
     - The student can also invoke the AI tutor chat at any time, even mid-question, to ask for help (if allowed by practice rules). Perhaps in a strict practice mode they might avoid that to simulate thinking themselves, but the option is there for learning mode.
     - Session results: When done, the student sees a summary: score (if applicable, though in practice mode it might just be % correct since not a full test), list of questions with their answers vs correct answers, and explanations readily accessible. They can review each one. They also see any performance stats from this session (time per question, etc.).

2. **Full-length Test Taking**

   - **Requirement:** Students can take a full-length ACT practice test under realistic conditions, and the system will time and score it automatically.
   - **Acceptance Criteria:**

     - The student (or teacher assigning) chooses one of the full tests. If the test is assigned by a teacher with a due date, the student should see that and be able to start it. If self-initiated, they pick which test or a random one.
     - Before starting, instructions are shown (just like the real ACT instructions for each section). The interface might mimic the ACT’s on-screen instructions if digital or show a unified instruction for paper-style.
     - The test is section-based. The system clearly shows the section name and has a dedicated timer for each. E.g., “English – 45:00 minutes”. On start, the timer counts down.
     - Within a section: navigation allowed among questions (like next/back). Possibly an index of questions so they can jump (but note: ACT on paper allows you to navigate within a section freely; a digital ACT might allow clicking question numbers). We should allow within-section navigation.
     - Mark for Review: student can mark questions and later jump back to them. The interface should highlight marked questions.
     - Answer selection: For multiple-choice, clicking an option selects it (and they can change answer until they submit the section). For the essay, a text box is given (with basic text editing features and a word counter).
     - Section Submission: When time is up, the section auto-submits (warn with 5 minutes remaining perhaps). The student can also end the section early if done. Once a section is done, they move to the next. They cannot return to a previous section (simulate real test rules). If doing an untimed or practice-oriented session, perhaps allow revisiting, but in realistic test mode, no.
     - After all sections, the test is completed. If a Writing essay was included, that might be scored by AI or given feedback later (within seconds or minutes, the AI can generate a score and some comments).
     - Scoring: Immediately upon completion, the platform calculates the raw score (# correct in each section) and converts to scale scores (1-36 for each section and composite). The conversion may use ACT-like conversion tables (which could be static or approximated). For example, 55/75 in English might map to a 23. We should have an algorithm or table for each test form. If the test is adaptive or random, a generic estimation could be used.
     - Results display: Show the student their section scores and composite. Offer to view detailed results. Possibly hide correct answers initially to mimic that in some official practice scenarios you might not get answer keys immediately (but since this is practice, likely we show them).
     - Upon viewing results, list all questions with correct answer and whether the student got it right or wrong. The student can click any question to see the explanation.
     - Save results: The test result (score, breakdown) is saved in the student’s history and contributes to their analytics. Teachers can see it in their dashboard too.
     - If the test was assigned, mark it as completed for that student. If late or some enforcement needed (like teacher wanted them to do it in one sitting at a certain time), some monitoring or at least time-stamp is recorded. (We might not implement full proctoring, but at least record start/end time).
     - Partial completion handling: If the student’s browser/device crashes or they need to pause, the system should ideally allow a resume (though for a real test simulation, pausing should not be allowed without teacher permission). Perhaps a teacher can allow a pause (for remote unproctored practice). At minimum, if accidentally closed, on re-login the student can continue where left off but the timer would have kept running to ensure no cheating of extra time (or we keep internal clock).

3. **Adaptive Practice (Smart Drills)**

   - _This is largely covered in adaptive difficulty section, but as a functional requirement:_
   - **Requirement:** In any practice session, the system adapts the sequence of questions to the student’s performance in real time.
   - **Acceptance Criteria:**

     - The selection algorithm fetches the next question after each answer rather than pre-loading all questions (to utilize performance data).
     - The algorithm has rules like: “If the last 3 questions were answered correctly in under 30 seconds each, consider increasing difficulty or switching to a new topic if mastery detected,” etc. These rules can be refined over time.
     - The adaptivity can be toggled off by a teacher (e.g., teacher-created quiz might want to be fixed content).
     - The system logs what difficulty level each question was and maybe an internal “ability estimate” for the student. This can be shown or hidden, but used to adjust next questions.
     - Students should not be aware of the adaptivity beyond perhaps noticing questions getting harder/easier; the interface doesn’t need to announce it. But if they reflect, maybe an optional stat “Your current practice difficulty level: Hard” can be shown for those curious.
     - The functional logic behind adaptivity should aim not to serve extreme difficulty differences abruptly (no whiplash of suddenly a super hard question after one easy correct answer; maybe ramp gradually).

4. **Explanations & Tutor Chat Access During Review**

   - **Requirement:** After answering questions (either in practice or after a test), students can access explanations and ask follow-up questions via chat.
   - **Acceptance Criteria:**

     - For each question in a review state, an “Explanation” button or link is available. Clicking it expands or shows the explanation text (which can include formatted text, equations if needed, etc.).
     - The explanation is comprehensive enough for self-study (fulfills the requirement of detailed reasoning).
     - A “Ask Tutor” or “Chat” option is present on the review page. If clicked, it opens a chat window/context where the AI is aware of which question (and the student’s answer) the student is asking about.
     - The student’s queries and AI’s answers are stored per session (maybe not permanently unless needed for analysis). But at least within that review session, they can scroll back in the chat.
     - The tutor chatbot can also be accessed generally (like a help icon anywhere to ask a question not tied to a specific practice question). That would be a general AI chat mode perhaps in the dashboard (“Ask our ACT Tutor anything”).
     - The chat should have safeguards: e.g., if the student asks for the answer to an assignment that’s not allowed or tries to misuse it, the AI should handle gracefully (likely beyond scope to detail here, but mention we’ll use an appropriate moderated model).

5. **Assignment Management** (Teacher-Assigned Work)

   - **Requirement:** Teachers can create assignments that consist of selected practice questions, a quiz, or a full test, and assign them to students with a due date. Students complete them and teachers review results.
   - **Acceptance Criteria:**

     - Teacher UI allows “New Assignment”: they choose type (e.g., Quiz or Test), select content:

       - For a quiz: pick X questions manually from the bank or specify criteria to auto-select (like “10 random hard questions from Math”).
       - For a test: pick one of the full-length tests or have system generate one on-the-fly for that class.
       - Possibly assign a _section_ of test or a custom set (like only a Math section of 60 questions as an assignment).

     - Set a due date/time and which students or class it goes to. Possibly allow timed vs untimed specification.
     - Students get a notification of the assignment and see it in a “Assignments” page or on dashboard (“Due Friday: Quiz on Algebra”).
     - Students complete it similarly to self-initiated practice/test. The difference is teachers can monitor if it’s done and see the score once submitted.
     - If past due, teacher sees who hasn’t completed. Possibly allow submission after due date with a late flag.
     - Teacher can manually score or override scores if needed (particularly for essay parts: if AI scored an essay but teacher wants to adjust, they should be able to).
     - After completion, teacher can provide feedback comments as noted. Students can see their grade/score for that assignment as given by teacher (which might incorporate things outside just correct count, e.g., teacher gives points for showing work if they had to upload something or partial credit—though our platform mainly auto-scores MCQ).
     - Functional: The system should differentiate these teacher-led assignments from personal practice in analytics (e.g., teacher can filter “show only independent practice vs assignments”).

6. **Time Tracking and Pacing**

   - **Requirement:** The system tracks time taken per question and section, providing data on pacing which is crucial for ACT.
   - **Acceptance Criteria:**

     - For each question, record how many seconds the student spent (especially in practice when immediate feedback is off, to simulate test behavior). Even in immediate feedback mode, time from question shown to answered is logged.
     - Summaries show average time per question in a section vs ACT average time. E.g., student took 45 min for 60 math questions (average 45 sec per question, which is good/bad relative to the 60 sec per question available).
     - In the analytics, highlight if a student consistently runs out of time or has a lot of leftover time (could indicate rushing or being too slow).
     - During practice, maybe a student can choose to have a timer per question as a training tool (like a visible countdown of 1 minute to answer each question, to train speed, but optional).
     - All timing data is stored and can be reviewed by teacher to advise on time management strategies.

7. **Multi-User (Class) Features** (if any additional like discussion or competition – optional)

   - This might be out of initial scope, but if included:
   - **Requirement:** Provide some collaborative or competitive practice features, like group quizzes or leaderboards, to increase engagement.
   - **Acceptance Criteria (if implemented):**

     - Leaderboard in class for points or questions solved (optional and resettable).
     - Group quiz games (maybe teacher starts a live quiz in class and students answer on their devices, Kahoot-style).
     - These aren’t core to requirements asked by user, so they can be noted as potential features but not mandatory.

Each of the above ensures the platform functions as intended for practice and testing scenarios, covering the lifecycle from content generation to a student’s answer and reflection.

### C. Study Plan and Personalization

Functional requirements related to generating and updating the study schedule:

1. **Initial Diagnostic & Plan Creation**

   - **Requirement:** Upon first use (or after a diagnostic test), the system generates a personalized study plan for the student.
   - **Acceptance Criteria:**

     - After completing a diagnostic full test (or entering a baseline score manually), the student (or teacher for that student) is prompted to “Generate Study Plan”.
     - The student is asked for their target test date (if not already provided) and target score (or this can be inferred if a teacher sets it or defaults to national average improvement, etc.).
     - The system outputs a plan (list of weeks/days with topics and tasks) as described. The plan should cover all sections, with emphasis on weaker areas.
     - Plan is presented to student for review. They can accept or ask for modifications (like “I want weekends off” or “I can study more hours”). Possibly a short wizard where student indicates how many hours per week they can devote.
     - The plan is stored and visible on the student’s Study Plan page. It should also be visible to their teacher.

2. **Ongoing Plan Adjustment**

   - **Requirement:** The study plan updates based on progress and performance.
   - **Acceptance Criteria:**

     - If a student completes tasks faster than planned, the plan marks those tasks done and can either pull next week’s tasks sooner or suggest additional practice.
     - If a student misses tasks, those are flagged and rescheduled (the system might push them into the next week or rearrange future tasks to accommodate). Possibly notify the teacher if a student falls too far behind schedule.
     - After each new test or significant milestone, the plan is re-evaluated. E.g., if a mid-point practice test shows the student has now mastered some initially weak areas but is still weak in others, the remaining weeks of the plan could be rebalanced to focus accordingly.
     - The student/teacher can manually trigger a plan recalibration at any time (like “Update my plan based on latest performance”).
     - The plan remains realistic (don’t suddenly add 10 hours of study in a week out of nowhere; if the required effort to meet target is too high, perhaps the system flags that the goal or timeframe might be unrealistic, and either suggests adjusting goal or acknowledges risk).

3. **Task Management**

   - **Requirement:** Each element of the study plan is treated as a “task” that can be checked off, tracked, and linked to platform actions.
   - **Acceptance Criteria:**

     - Examples of tasks: “Complete Practice Test 2”, “Do 30 math questions on Algebra”, “Review flashcards for 15 minutes”, “Read grammar guide on punctuation”.
     - For tasks that correspond to platform actions (like completing a test or questions), when the student does those actions, the task automatically marks as done. (E.g., if they just finished Practice Test 2, the system knows and marks that task complete on their plan).
     - For tasks that are outside (like reading a guide or outside study), the student can manually mark them done.
     - Task items have due dates (could be by end of week or specific dates).
     - The study plan view shows overdue tasks, upcoming tasks, and completed tasks (with strike-through or checked).
     - Teachers can also mark or verify tasks (maybe teacher assigns some offline homework like “complete this worksheet not on the platform”; teacher can mark it done for the student in the system, or input a note).
     - Students can defer a task with reason (like if something came up, they can push it by a couple of days – the system will then adjust subsequent tasks).

4. **Multi-Platform Notifications**

   - **Requirement:** The system should remind students of their study plan tasks via various channels.
   - **Acceptance Criteria:**

     - In-app notifications: When a student logs in, a reminder like “You have 2 tasks due today” or a daily pop-up of tasks.
     - Email notifications: Option to receive a daily or weekly email summary of tasks. E.g., Monday email: “This week’s study plan for you: …”. And/or a reminder the night before a test assignment due date.
     - Push notifications (if mobile app): e.g., at 7pm, “Time to study! You have a Reading practice due tomorrow.”
     - Teachers/admins can get alerts if a student hasn’t logged in for a long time or is consistently missing tasks (so they can intervene).
     - All notifications are configurable (user can opt out or adjust frequency, and abide by privacy preferences, especially emailing minors – likely to the email they signed up with or a parent if provided).

5. **Goal Setting and Tracking**

   - **Requirement:** The system should allow setting goals (target score and intermediary goals) and track progress toward them as part of the study plan.
   - **Acceptance Criteria:**

     - The student’s target composite score is recorded (and maybe target section scores if desired). The study plan is essentially built to reach that.
     - On the dashboard or plan page, show progress: e.g., “Current: 25, Goal: 30” with a progress bar indicating how far.
     - If a student reaches a goal early, celebrate it and allow setting a new higher goal if time permits, or shift focus to maintaining skills.
     - If it becomes apparent the goal is unlikely (e.g., test is next week and student is far off), maybe gently signal this to teacher to discuss with student. The platform might not auto-change goal but could suggest adjusting expectations.
     - Support multiple goals: content goals (like “improve in Science section by 5 points”) or process goals (“complete 1000 practice questions”). These could be optionally set by students or teachers to gamify and motivate.

6. **Teacher Involvement in Study Plans**

   - **Requirement:** Teachers can view and edit their students’ study plans to ensure they align with class activities or tutoring sessions.
   - **Acceptance Criteria:**

     - Teacher can pull up any student’s plan, see all tasks.
     - Teacher can add a task (e.g., “Attend Saturday workshop at school”). These could be flagged as teacher-added.
     - Teacher can adjust difficulty or focus if they have specific insight (like override the algorithm’s suggestion by adding more reading comp practice because the teacher knows that’s coming up in class).
     - If a teacher changes a plan, the student gets notified and the plan re-syncs (and perhaps the AI doesn’t override those changes in the next auto-update unless clearly needed, or at least prompts if conflict).
     - Teachers might also lock certain tasks (like “Full Test on date X” which is a class simulation test – the plan should revolve around that fixed event).

7. **Content Recommendations**

   - **Requirement:** Based on the study plan and student performance, the system should recommend specific content to focus on. (This overlaps with adaptivity, but is more proactive suggestions.)
   - **Acceptance Criteria:**

     - The platform might have a “Recommended for you now” section: e.g., “Practice Science section – last test indicates this is your lowest. We suggest taking a timed Science section today.” Or “You have trouble with Trigonometry; review this lesson and do these 5 practice questions.”
     - These recommendations tie into the plan but can also be spontaneous if the student wants something to do outside the scheduled tasks.
     - For example, after finishing a quiz, it might say: “Recommended next: Do 10 more questions on topics you missed.” with a button to start those.
     - The student is free to follow or ignore recommendations, but they are there to guide additional practice.

These functional requirements ensure the study planning is actionable and tailored, not just a static schedule.

### D. Analytics and Reporting

Functional requirements for the analytics discussed:

1. **Score and Performance Reports**

   - **Requirement:** The platform shall generate reports of student performance at different levels (individual, class, school).
   - **Acceptance Criteria:**

     - Student-level: A report that includes all test scores, best scores, average, breakdown by section, list of completed assignments and scores, etc. This can be shown on screen and exported as PDF.
     - Class-level: Teacher can generate a report for a class for a time period (e.g., last month) with each student’s improvement and average scores. Possibly include distribution charts.
     - School-level: Admin can generate a report summarizing all classes, maybe comparing classes, etc.
     - Reports can be filtered by date range, by type of activity (only full tests vs all practice).
     - The system should allow scheduling automatic reports (maybe an admin gets a monthly summary email report, teacher gets a weekly class summary by email).
     - Reports should include visual elements if possible (graphs) and interpretations (maybe even auto-generated summary like “Class A improved by an average of 2 points in Math this quarter”). That auto-summary could be a nice AI use as well.

2. **Item Analysis and Question Insights**

   - **Requirement:** Provide analytics at the question/item level to help improve content and identify trends.
   - **Acceptance Criteria:**

     - For content managers and perhaps teachers: see statistics for each question (how many students attempted, percentage who got it right, common wrong answers).
     - This can flag if a question is too hard or possibly misleading (e.g., if only 10% got it right and top students also missed it, maybe the question or explanation needs review).
     - Teachers can see item analysis for their class on an assignment (e.g., Question 5: 30% correct, many chose B instead of A, indicating a misconception to address).
     - Content manager dashboard might highlight “20 questions with <30% correct rate” for review or “questions that many students report as confusing” (if we have a feedback mechanism on questions).
     - These insights feed back to improving content and teaching focus.

3. **Progress Trends & Predictions**

   - **Requirement:** Use analytics to predict outcomes and highlight trends.
   - **Acceptance Criteria:**

     - The system might use machine learning on performance data to predict a student’s likely ACT score range if they continue at the current pace, or how likely they are to hit their target. This could be shown to teachers (with caution) to identify who needs more help.
     - Show trends: e.g., a graph of score vs study time to see correlation.
     - Possibly a feature to “simulate improvement”: if a student increases study time or improves X skill, how might that affect their score? (Though this might be beyond MVP, it’s an interesting analytic tool).
     - The platform can also identify anomalous trends (like sudden drop in performance, indicating the student might have not tried on a test or something; teacher can inquire if okay).

4. **Real-time Monitoring**

   - **Requirement:** For proctored or live scenarios, allow teachers to monitor progress in real-time.
   - **Acceptance Criteria:**

     - If a teacher sets a class to take a practice test in class, they could have a live dashboard that shows who is on which section, how much time left for each, maybe number of questions answered so far. This is akin to a proctor’s view to ensure all started, etc.
     - Not a primary need, but helpful for in-class use.
     - Could also simply show who is currently online and practicing, for engagement tracking.

5. **Usage Analytics** (System usage, not just performance)

   - **Requirement:** Track and report on user engagement metrics.
   - **Acceptance Criteria:**

     - Number of hours studied per student per week (for teacher to see and motivate or for admin to measure usage of the product they bought).
     - Feature usage: how often is the AI tutor used, how many questions are being generated by the AI vs manual use, etc.
     - System should log these events and allow generating metrics like “On average, students ask 3 AI tutor questions per test” – not that the end user needs that, but product managers might use it as KPI (e.g., engagement with AI features).

6. **Data Export & API**

   - **Requirement:** The platform shall allow exporting analytics data for external use.
   - **Acceptance Criteria:**

     - CSV export of scores, or an API endpoint where an admin can fetch student data (with secure token).
     - Ensure only authorized use – e.g., a school might want to integrate with their own data dashboards, so they use an API key to pull data.
     - Also compliance: allow a full data export of a single student’s data if they request it (for data portability under GDPR, etc.).

By fulfilling these, the platform makes data actionable and useful, not just collected. Teachers and admins can clearly see the impact and make informed decisions.

### E. User Management and Administration

Now, functional requirements for managing users, roles, and settings:

1. **Account Creation and Onboarding**

   - **Requirement:** Users can be added to the system either via self-registration (for individual sign-ups) or by administrators/teachers (for schools).
   - **Acceptance Criteria:**

     - Self-registration flow for students/tutors who come to the website: They provide name, email, password, possibly some profile info like school or target test date. A verification email is sent. They choose if they are a student or educator (which might influence account type creation and what they see first). If educator, maybe they have to provide school or organization details.
     - Bulk registration: An admin can upload a list of student emails (and optionally names) to invite them. The system sends out invite links. Similarly for teacher accounts.
     - Teachers can invite students by email to join their class (the student clicks link, creates account if not existing, then automatically joins the class).
     - Single sign-on: If integrated with Google/Microsoft, users can sign in with those without separate password. (In that case, the first time might auto-create an account tied to that email domain if allowed).
     - On first login, user is guided through setting up profile: for students, set target score/date, maybe take diagnostic (or schedule it); for teachers, maybe create first class or explore content; for admin, overview of how to add others.
     - Provide a brief tutorial or tour of the interface on first use.

2. **Class/Group Management**

   - **Requirement:** Teachers and admins can organize students into classes or groups for easier management.
   - **Acceptance Criteria:**

     - Teacher can create a “class” (e.g., “ACT Prep Period 1” or “Tutoring Group Alpha”) and either invite students or assign existing student accounts to that class.
     - Students can be in multiple classes if needed (though for ACT maybe typically one group, but maybe a student could have a school class and also a private tutor – could they be linked to both? Possibly yes, so system should allow that, with appropriate data sharing boundaries if so).
     - Admin can view all classes in their organization, create new ones and assign teachers to them (like set up structure if needed).
     - Removing a student or teacher from a class should not delete their account, just update relationships.
     - If a teacher leaves, admin can transfer their classes to another teacher or take ownership temporarily.
     - A student not in any class could be considered “independent learner” and still have full features, but an admin might prefer all students be under some teacher’s supervision.

3. **Permissions & Role Changes**

   - **Requirement:** Admins can change user roles or permissions if needed.
   - **Acceptance Criteria:**

     - Admin (system or org) can promote a teacher to also be a content manager or admin for that org, etc., via an admin panel. Or demote roles.
     - There should be safeguards (e.g., only system admin can make someone else system admin; org admin can’t escalate beyond their scope).
     - If a teacher tries to access admin-only section, the UI should prevent it (ideally such sections not visible unless permission exists).

4. **Settings Management**

   - **Requirement:** Provide an interface for various settings at user and org level.
   - **Acceptance Criteria:**

     - Profile settings for each user: name, contact info, notification preferences, password reset, profile picture maybe.
     - Org Admin settings: manage school name, time zone, default settings (like enforce a particular content set, or turn off some features if they want; e.g., maybe a school wants to disable the AI chatbot for whatever reason – should that be allowed? Possibly).
     - Integration settings: For admin to set up an LMS integration or SSO (they might need to input their LMS keys or configure LTI keys etc.).
     - Content settings: Possibly toggles like “enable experimental adaptive mode” or “use easy mode only” – but those might be more system side.
     - Subscription management (if relevant): see license count, renewal date, etc., though that might be only system admin or org admin if on self-service model.

5. **Logging and Audit (Admin view)**

   - **Requirement:** Administrators can view logs of key actions for auditing.
   - **Acceptance Criteria:**

     - A log of user logins, assignment completions, content changes, etc., accessible by system admin (and maybe org admin for their users).
     - This might not be fully exposed in UI aside from support tools, but should exist behind scenes at least.
     - Useful for debugging issues or investigating if a student claims something like “I did take that test, it didn’t record” – admin can see if it started, etc.

6. **Support and Help**

   - **Requirement:** Built-in help features for users and a channel to get support.
   - **Acceptance Criteria:**

     - A help center or FAQ section accessible to users (maybe content manager writes tips like “How to interpret your dashboard” or “How to use study plan effectively”).
     - For product support: a way to contact support (could be as simple as an email link or form within platform, or a chat if provided). This would be handled by support team (not the AI tutor, since that’s academic help).
     - These aren’t directly product “requirements” but more service, yet including them because a comprehensive product would have them.

Completing these functional requirements ensures that the platform’s features are fully realized in how users interact with the system.

Next, we consider the non-functional requirements that define the qualities and constraints of the system.

## Non-Functional Requirements

Non-functional requirements (NFRs) describe the qualities, performance, and constraints of the system. They ensure that beyond just doing what it should, the platform does so efficiently, securely, and at scale. We outline NFRs in categories such as scalability, performance, availability, security, usability, maintainability, etc.

### 1. Scalability

- **User Load:** The system shall scale to support a growing number of users (students, teachers, etc.) without degradation of performance. It should handle, for instance, at least **10,000 concurrent student users** during peak times (e.g., an entire school district having students practice in the evening) and be easily scalable beyond that by adding resources.
- **Content Scaling:** The architecture should accommodate a very large question bank (tens of thousands of questions) and many simultaneous content generation requests. As AI generation could be resource-intensive, the design should allow scaling the AI generation service separately (e.g., running multiple instances or using cloud functions) to handle spikes (like when many teachers generate tests at semester start).
- **Geographical Scaling:** If serving users in different regions, the system should use CDN or data centers in multiple regions to reduce latency (especially for content like images or videos in explanations). The design might consider multi-region deployments for both performance and redundancy.
- **Database Scalability:** The data storage solution should handle increasing data volume (user data, results, logs). Use of efficient indexing, partitioning, or sharding should be considered once data grows large. The system should not experience slow queries even as millions of answer records accumulate.
- **Stateless Services:** Backend services should ideally be stateless (session info stored client-side or in a distributed cache) to allow easy horizontal scaling (spin up new instances behind load balancer).
- **Auto-scaling:** In cloud deployment, use auto-scaling rules for critical services (e.g., if CPU or queue length for AI generation increases, automatically add instances).

### 2. Performance

- **Response Time:** The platform should be responsive. Target:

  - Page loads (dashboard, etc.) within **3 seconds** on average networks.
  - When a student submits an answer, feedback (if immediate mode) appears within **1 second**.
  - After finishing a full test, the score report generation should take no more than **5-10 seconds** (including AI scoring any essays), ideally faster.
  - AI tutor responses should be generated in a conversational acceptable time, e.g., within **2-5 seconds** for typical questions, up to 10 seconds for very complex queries. If it takes longer, the UI should indicate it’s working.

- **Throughput:** The system should handle high throughput for certain actions. For example, if 1000 students all start a test at exactly 9:00 AM (like a mock test event), the system must handle scoring all of them around 10:30-11:00 when they finish, which could be heavy. Similarly, if multiple teachers generate content simultaneously, the AI backend should queue and process these efficiently (maybe dozens of generation requests per minute).
- **Data Refresh Rate:** Analytics dashboards should update with minimal lag. If a student finishes a test, the teacher’s view should reflect the new score ideally within seconds (real-time push or quick polling).
- **Lightweight UI:** The front-end should be optimized (minified assets, limited heavy scripts) to work even on school-provided low-end laptops or older browsers. It should degrade gracefully if WebGL or fancy features not supported.
- **Efficient Algorithms:** Adaptive learning algorithms and scheduling should run in a timely manner (e.g., recalculating a study plan should be near instantaneous on user action, since it’s not huge data – can be done either in client or quick server call).
- **Resource Usage:** Efficient use of server resources for cost and performance—e.g., caching frequently accessed data (like question content that is used by many students) so we don’t hit DB repeatedly, especially for static content or images.

### 3. Availability and Reliability

- **Uptime:** The service should be highly available, targeting at least **99.5% uptime** or higher (which translates to at most \~3.65 hours of downtime per month). Ideally, aim for 99.9% if budgets allow, since educators may rely on it for scheduled classes.
- **Redundancy:** No single point of failure. Use redundant servers for each component (multiple app servers behind load balancer, replicated databases or read-replicas, etc.). Use cloud managed services or clusters for DB to ensure failover.
- **Backups:** Regular backups of critical data (user data, results, content). For example, nightly backups of database with retention of X days. Also backup of any AI model or configurations if self-hosted (so those can be recovered).
- **Disaster Recovery:** In case of major outage or data loss in primary region, have a plan to recover in a secondary region with minimal data loss. RPO (recovery point objective) maybe < 1 hour (data loss window) and RTO (recovery time objective) maybe a few hours to restore service in worst-case scenario.
- **Consistency:** Ensure that the system doesn’t lose track of user progress even if something fails mid-way. For instance, if a student is taking a test and something crashes, the system should ideally allow them to resume or at least not lose what they’ve done. Transactions like saving answers should be atomic and durable (so partial answers up to last submitted question remain).
- **Graceful Degradation:** If certain components fail (like AI tutor goes down because external API issue), the platform should still allow core usage (students can still take tests and get pre-existing explanations; maybe show a message that live tutor is unavailable). Essentially, non-critical features failing shouldn’t bring the whole system down.
- **Maintenance Windows:** Schedule maintenance (like updates) in off-peak hours and inform users ahead of time. Possibly implement rolling updates to avoid any downtime if possible.

### 4. Security

- **Data Encryption:** All communications must be over HTTPS/TLS. No plaintext traffic. Sensitive data in the database (like personal info, or any access tokens) should be encrypted at rest.
- **Secure Coding:** Protect against common web vulnerabilities: SQL injection (use ORMs/prepared statements), XSS (proper output encoding and Content Security Policy), CSRF (CSRF tokens on forms or same-site cookies), etc. Use security testing and code reviews regularly.
- **Authentication & Authorization:**

  - Use robust authentication (e.g., OAuth 2.0 standards for SSO). Passwords stored hashed with a strong algorithm (bcrypt or Argon2).
  - Implement account lockout or captcha after repeated failed logins to prevent brute force.
  - Ensure JWT or session tokens are properly secured (http-only cookies, short expiration with refresh).
  - Authorization checks on every API call based on user roles, to prevent one user accessing others’ data by simply altering identifiers in requests, etc.

- **API Security:** If external APIs are exposed for data, secure them with API keys or OAuth and have rate limiting.
- **Logging & Monitoring:** Log security events (login attempts, changes in privileges, unusual activity) and monitor them. Possibly integrate with a SIEM (security info and event management) if used by company.
- **Penetration Testing:** Periodically have the system tested for vulnerabilities by internal or third-party. Fix any issues promptly.
- **Privacy Protections:** Ensure that even internal team access to personal data is restricted (for example, developers shouldn’t casually access student data in production; use role separation and auditing if they need to for support).
- **Data Isolation:** If the SaaS serves multiple client organizations (schools, companies), ensure their data is separated logically (through tenant IDs or separate databases schemas) to avoid any chance of one school seeing another’s data. Multi-tenancy should be designed securely.
- **Secure AI Usage:** If using third-party AI APIs, ensure compliance with their security terms (e.g., not sending sensitive info) and use encryption for data in transit to them too. If AI model is self-hosted, ensure it’s on secure infrastructure and cannot be misused or queried externally without auth.
- **Regular Updates:** Keep all software libraries and systems updated to patch security vulnerabilities. This includes web frameworks, database, OS, etc.
- **Compliance Measures:** Adhere to **FERPA** and other laws by design: e.g., have a procedure to delete student data upon request or after a certain period of inactivity (if required by policy), ensure any third-party sub-processors (like cloud hosts or AI API providers) sign data protection agreements.

### 5. Usability and Accessibility

- **Ease of Use:** The platform should be intuitive for tech-savvy and not-so-tech-savvy users alike. Use standard UI patterns, clear labeling, and provide tooltips or help text for anything not obvious.
- **Accessibility (ADA/WCAG Compliance):** Aim to meet **WCAG 2.1 AA** standards:

  - All functionalities available via keyboard (important for users who can’t use a mouse).
  - Support screen readers: proper semantic HTML, ARIA labels for dynamic content, etc.
  - Ensure color choices have sufficient contrast. Avoid relying solely on color to convey information (e.g., wrong answers not just highlighted in red but also with an icon or text).
  - Provide captions or transcripts for any audio/video content in the platform (like if an explanation has a video).
  - Allow font size adjustment or zooming without breaking layout.

- **Performance on Low Bandwidth:** Optimize so that even users with slow internet (some rural schools, etc.) can use the platform. Possibly provide an option for a “low bandwidth mode” that maybe loads fewer animations or high-res images.
- **Cross-Browser Compatibility:** Support latest versions of major browsers (Chrome, Firefox, Safari, Edge) and the default browsers on school-issued devices (which might be older or locked-down versions). Also ensure mobile web works on Safari iOS and Chrome Android well if no native app.
- **Localization Support:** While initial focus might be English, design should not hard-code text (so it can be translated if needed). Also, consider numeric formats or date formats if international.
- **User Feedback Mechanism:** Provide easy ways for users to give feedback on content or usability (like “Report a problem” on a question if the explanation is unclear, or “Suggest a feature” somewhere). This data goes to product team for improvement.

### 6. Maintainability & Extensibility

- **Modular Architecture:** The system should be built in a modular way (both in code and deployment) such that components can be modified or replaced without affecting the whole system. For example, the AI engine could be swapped out if needed (maybe today using GPT-4 API, tomorrow a custom model) by altering just the AI service module.
- **Clean Code and Documentation:** The codebase should follow clear coding standards, with documentation for APIs and major modules, so future developers or teams can easily onboard and extend. Comments and design docs should be available for complex logic like the adaptive algorithm.
- **API-First Approach:** Where applicable, backend APIs should be designed for reuse (maybe a future mobile app uses the same APIs, or third parties integrate). This naturally enforces separation of concerns and easier maintenance (front-end and back-end decoupled).
- **Testing:** There should be an automated test suite (unit tests for logic, integration tests for critical flows like taking a test, maybe UI tests for common actions). This ensures that changes don’t break existing functionality (critical for a stable product).
- **Logging & Monitoring:** Comprehensive logging (with different levels) helps maintainers debug issues. Integration with monitoring tools (like New Relic, DataDog, or even cloud provider monitors) to track system health (CPU, memory, errors, response times).
- **Continuous Integration/Delivery:** The development process should include CI/CD so that new releases can be deployed frequently and reliably. This means automated build, test, and deploy pipelines.
- **Extensibility:** Design with future features in mind. For instance:

  - If later adding SAT prep as another exam, how easily can the question generation adapt to that? Perhaps design the data models to not be strictly ACT-only (e.g., a question could have an exam type field).
  - If adding gamification or social features, is there a place to plug those in without a complete refactor?
  - Use configuration files or admin settings for things that might change (like number of questions in a section, in case ACT changes format, so it’s not all hard-coded).

- **Versioning:** If exposing APIs or if content has versions, manage versioning to not disrupt older clients. Also migrating the database or models should be done with backward compatibility in mind when possible.

### 7. Cost and Efficiency (if relevant)

- **Infrastructure Cost Optimization:** As a SaaS, running costs should be monitored. Use auto-scaling to also scale down when low usage to save cost. Choose cost-effective services (e.g., using serverless for AI generation if it’s spiky might save running an always-on expensive GPU instance).
- **AI Usage Optimization:** If using paid AI API calls, implement caching of results where possible (maybe if many students ask similar questions, although that might be rare; more likely caching content generation outputs if reused). Possibly batch requests if dozens of similar content needed at once.
- **Licensing:** Ensure any third-party software or data (like maybe using some licensed ACT materials or a library for equation rendering) is properly licensed and costs accounted for at scale.

### 8. Compliance and Standards

- **Standards Compliance:** The system should comply with any relevant interoperability standards:

  - LTI for LMS integration (like LTI 1.3 Advantage).
  - QTI (Question and Test Interoperability) possibly for question formatting if integrating/exporting content (if we want to export questions or import from other sources that use QTI XML, design with that possibility).
  - Accessibility standards as noted (WCAG).

- **Legal Compliance:**

  - Data privacy laws: **FERPA, COPPA, GDPR, CCPA**, etc. These were touched on in security but as NFR: the system must have features to meet these (like parental consent tracking for COPPA if needed, data export/delete for GDPR, not storing data in certain jurisdictions if policy says so, etc.).
  - Content copyright: Ensure AI-generated content does not inadvertently plagiarize copyrighted material. We might want a check that generated questions aren’t verbatim from some known source (hard to ensure, but maybe part of content manager review).
  - Accessibility (again, legal side: ADA or equivalent education laws requiring accessible technology).

- **Educational Standards Alignment:** As a non-functional aspect, ensure content _coverage_ meets ACT specs. For example, if ACT says 40% of English questions are punctuation, our question bank should roughly reflect that distribution. This is more a content requirement, but one could see it as a quality standard to adhere to. Possibly run periodic analyses of the question bank to ensure balance.

Non-functional requirements are crucial for user satisfaction and trust: a platform that crashes or leaks data would fail no matter how good the features are. Thus, these NFRs must be given equal weight in development planning.

## Technical Architecture

This section describes the proposed technical architecture of the platform, including its major components, their interactions, and technology choices. It covers the division between frontend and backend, the integration of AI models, data storage design, and how third-party integrations fit in. A high-level architecture diagram is provided for clarity, followed by explanations of each component.

&#x20;_High-level architecture diagram illustrating the platform components and data flow._

_(Diagram Description: The diagram shows Users (Students, Teachers, Admins) accessing the platform via Web or Mobile App. The app communicates with a backend (API Server). The backend is composed of microservices or modules: Authentication Service, User Management, Content Generation Service (which connects to an AI Model), a Content Repository (database of questions/explanations), a Test/Quiz Service, an Analytics & Reporting module, and Integration connectors (LMS, Email, etc.). All services read/write to appropriate databases (User DB, Results DB, Content DB). The AI Model (LLM) may be external (cloud AI API) or internal. The architecture ensures separation of concerns, scalability, and security boundaries between components.)_

### 1. Frontend (Client-side)

- **Web Application:** A single-page application (SPA) built with a modern framework (e.g., **React**, Angular, or Vue). React is a strong candidate due to its popularity and rich ecosystem. The web app delivers the user interface for all roles (with role-based rendering of features). It communicates with backend via HTTPS (RESTful APIs or GraphQL). The SPA approach ensures a snappy, interactive experience (feels like an app rather than reloading pages). Also, components can be reused for different parts of the app (e.g., a question rendering component used in practice and in test review).
- **Mobile Application:** Two approaches:

  - Responsive Web: The web app is responsive to different screen sizes, so it works on mobile browsers as well. Initially, this might be sufficient.
  - Native/Hybrid App: Optionally, a dedicated mobile app (built with React Native or Flutter for cross-platform) could be developed for better offline support and push notifications. This app would use the same backend API.

- **Key UI Components:**

  - Dashboard pages for each role (as described in UI section),
  - Test-taking interface (with timer, etc.),
  - Study Plan calendar,
  - Admin console pages,
  - Content editor (for content managers; maybe this is separate or hidden for most users),
  - Chatbot interface (likely a chat widget component).

- **State Management:** Use a predictable state management (like Redux for React) to handle complex state like test questions, timer countdown, analytics data etc. This ensures the app remains manageable as it grows.
- **Front-end Optimization:** Use code-splitting to only load heavy components when needed (e.g., content editor tools only for content managers), to keep initial load fast for students.
- **Security on Frontend:**

  - Ensure JWT or session token is stored securely (probably httpOnly cookie to avoid XSS stealing it, or secure storage if using mobile).
  - Use front-end routing to protect routes by role (also will be enforced by backend but nice UX to not even show unauthorized links).
  - Input validation on forms before sending to reduce round trips (though backend will re-validate).

### 2. Backend (Server-side)

The backend can be structured as microservices or a modular monolith. Given the diverse functionality, a service-oriented approach is likely beneficial for scaling different parts independently. Key backend components/services:

- **API Gateway / Backend-for-Frontend:** A single endpoint (or unified server) that the frontend communicates with. This could be an API gateway that routes calls to appropriate microservices. Alternatively, we use a GraphQL server that federates to services. But more straightforward: a set of RESTful endpoints grouped logically (auth, content, analytics, etc.).
- **Authentication Service:** Manages user accounts, login, JWT issuance, password resets, OAuth integration, etc. Could be a standalone service or just a module. For SSO, it handles redirect flows or token validation from Google/Microsoft. Also handles role info in user profile.
- **User Management Service:** CRUD for user profiles, classes, roles. Also handles invitations to platform. Might overlap with Auth service or be integrated.
- **Content Generation Service (AI Service):** This service interfaces with the AI model. For example, when a request comes to generate questions, this service formulates the prompt to the LLM, calls the AI API, and gets results. It may include some logic to parse AI output into structured question format. It might also use auxiliary AI models (like a simpler model to classify the difficulty of the generated question).

  - If using external API (OpenAI, etc.), it must handle API keys and rate limiting.
  - Could be designed to queue requests if needed (some may take a few seconds, so better not to keep web request open too long; possibly handle via asynchronous jobs and poll or webhooks when done).

- **Content Management Module:** Responsible for storing questions, tests, etc. Likely this is an internal API to the content database. It provides methods to fetch questions by criteria, save new questions, update them, etc. If microservices, it might be part of a larger “Content Service” that includes generation and storage both; or separate but closely linked.
- **Test/Quiz Service:** Manages test definitions and grading logic. For auto-scored sections, it tallies scores. For essays, it might call the AI scoring function. It also tracks test sessions (to resume if needed). Might have sub-component for “Timing & Session Mgmt” to handle the live aspects (maybe using WebSockets to sync timers or just rely on client timers with server verification).
- **Analytics Service:** Aggregates performance data. This might involve a specialized data store optimized for analytics (like a separate database or even using a data warehouse for heavy analysis if needed). But for real-time, probably a service that queries the main DB or a cache of precomputed analytics. Over time, might implement background jobs to compute stats (like nightly computing each student’s up-to-date mastery level or generating the weekly reports).
- **Notification/Email Service:** Handles sending emails or notifications. Could integrate with an email API (SendGrid, etc.) for emails, and push notifications via Firebase or similar for mobile- **Database & Storage:** The platform uses a reliable relational database (e.g., **PostgreSQL**) to store structured data: user profiles, class enrollments, test results, etc. There might be separate logical databases or schemas for:

  - **User & Results Data:** Stores user information, role, class memberships, and all performance data (answers given, scores, analytics metrics). Proper indexing ensures quick retrieval of a student’s history or class reports.
  - **Content Data:** Stores questions, exams, and explanations. This could be in the same database or a separate one optimized for content queries. Each question record includes text, answers, tags, etc., as described. A search index (like Elasticsearch) might be used to allow keyword searches through questions if needed (for content managers searching for duplicates or specific topics).
  - **Study Plans / Schedules:** A table for study plan tasks (with fields for user, task type, due date, status) to easily query what tasks are due or completed.
  - If the system needs to store large media (images for math diagrams or video clips), a cloud storage (e.g., AWS S3) would be used with links stored in the DB. But primarily, ACT content is text-based, so storage needs are mostly for text and data records.

- **Caching Layer:** To improve performance, a caching system like **Redis** might be used. Example uses: caching frequently accessed data (e.g., the question bank or parts of it, so that repeated question fetches don’t always hit the DB), caching session data or recent analytics computations, and storing active test session info (for quick lookup of how much time is left if needed).
- **Background Job Queue:** The architecture should include a mechanism for asynchronous processing (e.g., **Celery/RQ** if using Python, or built-in queue in Node, or cloud services like AWS SQS with Lambda). This is used for tasks like:

  - Sending emails/notifications (to not block user actions).
  - Processing heavy analytics calculations (if we pre-compute some stats nightly).
  - Handling AI content generation requests if those are done async – for instance, a teacher requests 50 new questions; we could enqueue this and notify when ready, especially if using a slightly slower but cheaper batch process.
  - Scoring an essay with AI might also be done async if it takes a few seconds, and result made available after.

- **AI Model Integration:** The AI component is key:

  - Likely we use an external AI service (like OpenAI’s GPT-4 or similar) accessed via API for content generation and possibly for the chatbot. This means our backend Content Generation Service formats requests (prompts) and sends them over HTTPS to the AI provider, then parses the response.
  - We must secure the API keys and handle errors from the AI service gracefully (e.g., if it’s overloaded or returns an inappropriate result, handle via error message or filtering).
  - Optionally, in the future an in-house model could be deployed (on cloud GPU instances or using a service like Azure ML) – hence the architecture should keep the AI as a separate component (so we can switch from external API to internal model by changing the implementation of that service without affecting other parts).
  - We may incorporate additional AI models: e.g., a smaller classification model to rate question difficulty or check content. These could be hosted via a microservice or even as a function in the Content Service.

- **Security & Access Control:** The backend enforces role-based access on all endpoints. We might use middleware to check JWT tokens and attach user roles to requests, ensuring e.g. a student trying to access an admin API gets denied. Data-level security is also enforced in queries (for instance, when a teacher requests student data, the query ensures it’s only for students of that teacher’s classes).
- **API Design:** Likely RESTful endpoints such as:

  - `POST /api/auth/login`, `POST /api/auth/ssologin` (for SSO callbacks),
  - `GET /api/students/{id}/dashboard`, `GET /api/students/{id}/progress`,
  - `POST /api/classes/{id}/assignments` (create an assignment),
  - `GET /api/content/questions?topic=geometry`,
  - etc.
    Alternatively, a **GraphQL** API could allow the client to request exactly the data it needs (this could be useful for flexible analytics queries from the front-end). The choice can be made during design; REST is simpler to start with, GraphQL could be a future enhancement for complex data fetching needs.

- **DevOps & Deployment:** The system is likely containerized (using Docker) so that each service can run in its own container (for example, a container for the web server, one for the AI worker service, one for a worker processing queue jobs). Using a container orchestration like **Kubernetes** or cloud services (AWS ECS, etc.) to manage scaling and reliability of these containers is recommended.

  - Continuous Integration (CI) pipelines will run tests and build these containers on every update.
  - Continuous Deployment (CD) can deploy new versions with zero/minimal downtime (rolling updates).
  - Logging from all services can be centralized (using something like ELK stack or cloud monitoring).
  - Ensure secrets (DB passwords, API keys) are stored securely (in vaults or environment configs not in code).

**In summary,** the technical architecture is a cloud-based, modular system: a rich client-side application communicates with scalable server-side services (that encapsulate authentication, content generation, test delivery, analytics, etc.), which in turn rely on robust databases and external AI services. This separation of concerns allows the platform to be developed and scaled effectively – for instance, during peak usage the test delivery and analytics services can scale out to handle load, while the AI generation service might scale based on content creation demand.

## Integration Points with External Systems

To maximize the platform’s utility in real educational environments and to leverage existing tools, we plan integration points with various external systems and services:

- **Learning Management Systems (LMS):** The platform will integrate with LMS platforms like Canvas, Schoology, Moodle, Google Classroom, etc. using industry standards. The primary method is **LTI (Learning Tools Interoperability)** compliance, which allows the ACT prep platform to function as an external tool in an LMS.

  - _LTI Integration:_ Teachers or admins can add the platform as an LTI tool in their LMS. This enables single sign-on: when a student launches the tool from the LMS, they are automatically logged into the ACT platform (the LMS passes the identity securely). It can also pass context like course/class and the user’s role.
  - _Roster Sync:_ Via LMS integration, the platform can import class rosters so teachers don’t need to manually invite students. For example, using LTI Advantage services or APIs, we can fetch the list of students in a course and auto-create accounts or map them to existing accounts.
  - _Gradebook Reporting:_ If desired, the platform can send back grades/scores to the LMS gradebook. For instance, when a student completes a teacher-assigned test, the percentage score or some point value could post to the LMS. (This would use LTI Assignment and Grade Services or an LMS-specific API).
  - The integration is configurable by the org admin – they input the necessary keys/credentials from their LMS into our platform’s admin settings to establish trust.

- **Authentication Services (SSO):** Many schools prefer students and staff use one set of credentials. The platform will support:

  - **OAuth2/OpenID Connect:** Integrations with Google (for Google Classroom users), Microsoft (Office 365/Azure AD), and possibly Apple ID for students on Apple devices. Users can click “Login with Google” and the system will authenticate via Google’s OAuth, creating or mapping to their account.
  - **SAML 2.0:** For enterprise/school SSO if they have their own identity provider (like OneLogin, Okta, or ADFS). The platform can act as a SAML Service Provider, allowing SSO integration that many school districts require. The org admin would upload their SAML metadata to configure.
  - These integrations ensure users don’t have to remember another password and that account management is centralized. All SSO logins still respect role mappings (for example, the system might map users from a certain AD security group to teachers, etc., as configured by admin).

- **Calendar and Notification Integration:** The platform can integrate with external calendar services:

  - Students can one-click **export their study plan** to Google Calendar or download an iCal file for Outlook/Apple Calendar. This populates their personal calendar with study tasks and exam dates, helping them manage time.
  - Reminder emails can be synced with email systems – e.g., if a school uses Gmail, email reminders will simply go to their Gmail; no special integration needed beyond ensuring deliverability.
  - Possibly integration with communication platforms like Slack or Microsoft Teams for notifications (for instance, a tutoring company might want notifications in a Slack channel when a student completes a test). This can be handled by webhooks or email-to-channel gateways.

- **Third-Party Content & Tools:**

  - **Video Lesson Providers:** Integration with video platforms such as Khan Academy or YouTube for explanations – e.g., the platform might embed a Khan Academy video on an algebra topic when showing an explanation or in the resource library. Technically, this is done via embed links; no deep integration, but we ensure we can play those videos in-app (honoring any required attributions).
  - **Dictionary or Encyclopedia APIs:** Possibly for a feature where a student can highlight a word in a reading passage and get a definition (integration with a dictionary API).
  - **Calculator Tools:** The ACT allows certain calculators. If a digital calculator tool (Desmos, etc.) is integrable, we might embed it in the math section for practice. For example, using Desmos’s API to include a calculator interface that mimics ACT’s allowed calculators.
  - **Text-to-Speech:** For accessibility, integrating with a TTS engine (maybe the device’s built-in or a service like AWS Polly) so that passages or questions can be read aloud to students who need it.
  - **External Question Banks:** If a tutoring company has its own item bank or the school has licensed official ACT practice questions in a digital format, we might provide import functionality (which is an integration of sorts). For instance, import from a CSV or QTI file exported from another system.
  - **Reporting and BI Tools:** Some administrators might want to pull data into their own analytics systems. While the platform provides built-in dashboards, we could integrate with Google Data Studio or PowerBI by providing connectors or at least easy export. For example, an admin could connect an API endpoint to their PowerBI to refresh data periodically for district-wide analysis.

- **APIs for Developers:** In addition to consuming other services, we expose certain APIs or webhooks so that third-party tools can interact:

  - For instance, a school’s portal might call our API to get a student’s latest ACT practice score to display on a centralized dashboard.
  - Webhooks: the platform can send an HTTP POST to a given URL when certain events happen (student completes test, or a study plan is generated). This allows custom integrations; e.g., a tutoring CRM receives a webhook and updates the student’s profile with their new score.
  - These are secured by secret tokens and only set up by admins who know what they’re doing. It essentially makes the platform extendable beyond our UI.

- **Email/SMS:** Integration with email/SMS gateways is straightforward:

  - Use an email service (like SendGrid, SES) for all system emails (account verification, password reset, notifications). Admins can customize the “from” address (especially for enterprise – e.g., [no-reply@schoolname.edu](mailto:no-reply@schoolname.edu)).
  - For SMS, integrate with Twilio or similar if we decide to send text reminders. (This might be optional and require phone collection with consent.)

By implementing these integration points, the platform becomes **interoperable** and can fit into existing workflows at schools and companies. A teacher can use it within their familiar LMS; students use their usual logins; admins can aggregate data in district dashboards – all reducing friction in adoption. Technical standards like LTI and OAuth ensure we’re not reinventing the wheel and can work with a broad variety of systems.

## Wireframes and UI Design for Major Workflows

Designing an intuitive user interface is crucial for engagement. Below we outline the UI/UX design requirements and mock-up concepts for major workflows for each user role. (Note: These are descriptions of wireframes and design; actual visual wireframes would accompany the document separately.)

### Student Interface

**1. Student Dashboard:** Upon login, a student sees a personalized dashboard. Key elements:

- **Greeting and Progress Snapshot:** “Hello Alex! Your ACT Goal: 30. You’re on track!” – a quick status line. Below it, prominent display of the student’s **current projected score** or last test score and how far it is from their goal.
- **Progress Charts:** Small charts or icons for each ACT section (English, Math, Reading, Science). For example, circular progress indicators showing current score or mastery percentage in each. Perhaps color-coded (red/yellow/green) to denote level of proficiency.
- **Upcoming Tasks:** A list or calendar view of study plan tasks due in the next few days. Each task listed with an icon (e.g., a pencil icon for a practice test, a book icon for reading an article). E.g., “📅 **Today:** Complete 20 Algebra practice questions (due by 9pm)”.
- **Quick Actions:** Buttons for primary actions: “Start Practice 🔄” (which might immediately begin an adaptive practice session), “Take Full Test 📝”, “Review Mistakes 🔍”, etc. These should be visually distinct, possibly as a menu or big icons.
- **Navigation:** A sidebar or top menu with sections: Dashboard, Practice, Tests, Study Plan, Performance, Resources (and a link to Support/Help).
- Clean layout with student-friendly, encouraging language. Not too overwhelming; highlights key info and one-click access to start studying.

**2. Practice/Test Interface:** When a student starts a practice session or test:

- **Layout:** For practice questions, a single-question view: question text at top, answer choices labeled A, B, C, D below it (possibly in radio-button style or card buttons). For reading, the passage would occupy a side or top section (scrollable) with questions on side or below.
- **Timer:** If it’s a timed full test, a timer is shown on screen, top corner (e.g., “Time Left: 30:25”). For untimed practice, no timer or maybe a stopwatch if we still record time.
- **Navigation & Tools:** Arrows or buttons for Next/Previous question (if allowed to move around). A “Mark for Review” toggle (star icon) on each question. Possibly an “Eliminate Choice” feature: in a UI, this might mean if the student right-clicks or long-presses an option, it grays out (to mimic crossing out).
- **Hint/Explain Buttons:** In practice mode, a “Hint” button might be at bottom. If clicked, a small pop-up or highlight appears with a hint. An “Explain” button might appear after the student submits an answer (in immediate feedback mode).
- **Submitting Answers:** For practice, maybe a “Check Answer” button to submit the single question. For full test, a “Submit Section” when they’ve answered all or time runs out (which then automatically transitions sections).
- **Design Considerations:** Use clear readable fonts (esp. for long reading passages or science graphs). Possibly show graphs or tables for Science as images – ensure they render well (with the ability to zoom if needed). The UI should be uncluttered to resemble a test environment – maybe neutral background, not too many distracting elements.
- **Post-Question Feedback (Practice mode):** If immediate feedback is enabled, once they answer, the option they chose is marked (like green if correct, red if incorrect, and the correct one highlighted if they got it wrong). Then the explanation text appears below. Also a “Ask Tutor” chat icon is available for follow-up questions on that item.

**3. Study Plan Page:** A dedicated view for the student’s schedule:

- Likely a **calendar view** (weekly agenda). Each day block shows tasks (colored by type perhaps). Clicking a day expands to show tasks with checkboxes.
- Alternatively, a simple list grouped by week: “Week 1 (Jan 1-7): \[ ] Task 1, \[ ] Task 2, ...”.
- Completed tasks are checked off and maybe moved to a “Completed” section or faded out.
- The student can adjust the plan here: maybe drag tasks to a different day, or click “+Add task” if they want to do extra.
- A “Regenerate Plan” or “Adjust Plan” button might allow them to tweak preferences.
- **UI should clearly show progress** – e.g., a progress bar of how many tasks done vs remaining this week.
- Also, perhaps a way to toggle between calendar and list.
- If integrated with calendar externally, show an icon to sync or a note “Synced to Google Calendar”.

**4. Performance/Analytics Page (Student):** This is where detailed analytics reside:

- Graphs of score improvement over time (line chart for each section score across tests).
- A breakdown by topic: possibly a table or chart. E.g., a bar chart listing topics (Algebra, Geometry, Trig, etc.) with percentage correct. Or a spider/radar chart showing proficiency in different areas of the ACT.
- Time management stats: maybe a table “Average time per question: English 30s, Math 45s, etc.” with an indication if that’s above or below recommended.
- The design should allow drilling down: e.g., clicking on “Geometry” bar could show a list of past geometry questions the student got wrong or link to practice specifically on that.
- It should also highlight strengths: perhaps a trophy icon next to topics where they consistently score very high (to celebrate mastery).
- The UI here is more data-heavy, so use visual cues: tooltips on charts to show exact values, ability to toggle certain metrics on/off (maybe checkboxes to show/hide certain lines on a graph).
- Keep color scheme consistent (e.g., English = blue, Math = red, etc. in charts) so the student recognizes sections easily.

**5. AI Tutor Chatbot:** Accessible via an icon (say a chat bubble) on all pages or at least on practice pages.

- When opened, a chat window overlays or pops up. It shows a conversational interface, similar to common chat UIs:

  - The bot’s messages and the student’s messages in a scrollable window.
  - A text input box at bottom for the student to type a question. Perhaps suggestions or example prompts to guide usage (“Ask me anything about the ACT or this question.”).

- If opened in context of a specific question, it might display that question (or a snippet) above for reference. The student’s question then appears, and the bot response shows after a few seconds.
- The design should make it clear this is a tutor help, e.g., call the bot “ACT AI Tutor” and use an icon like a friendly robot or an academic hat.
- The chat can also be accessed from the dashboard for general questions like “What’s a good strategy for ACT Science?” – then it’s just a normal chat without specific question context.
- Include an option to thumbs-up or thumbs-down responses so the student can give feedback if the explanation helped or not (this info can be logged for quality improvement).

Overall, the student UI design aims to be **engaging, clear, and motivating**. Visual elements like progress bars, badges, and a minimalistic test interface help keep focus. The color palette likely soft and academic (e.g., blues and greens) to be easy on eyes for long study sessions. Accessibility is considered: all interactive elements are large enough to tap, and there are alternative text for images, etc.

### Teacher Interface

**1. Teacher Dashboard (Class Overview):** After login, a teacher sees an overview of their classes:

- **Class List:** If multiple classes, a simple list or tabs with each class name. Each might have a quick stat like number of students and average score.
- **Class Dashboard:** Selecting a class shows aggregated info:

  - Average composite score of the class, perhaps a chart of distribution (e.g., a histogram of scores or pie of how many in each score band).
  - A list of students with key info in a table:

    - Name, last test score, improvement since first test, last login date, number of tasks completed vs assigned (to see who is keeping up).
    - The teacher can sort or filter this table (e.g., sort by score to see top performers or who needs help).

  - Alerts or reminders: e.g., “2 students haven’t logged in for >7 days” or “3 assignments due this week”.

- **Actions:** Buttons like “Create Assignment”, “Generate Test for Class”, “Message All Students” if messaging is included (or at least instruct to do via email outside platform if not built-in).
- Clean professional look, but still friendly. Possibly school branding visible if the account is tied to a school (like a logo or school name at top).

**2. Student Detail View:** Clicking a student from the class list opens their profile (what the teacher sees, which may have more info than the student’s own view):

- Shows the student’s photo or initials (if provided) and profile info (grade level, target score, etc.).
- Performance summary: their best scores, current trajectory. Possibly comparisons to class average (e.g., “Math: 28 (Class avg 25)”).
- Breakdown of strengths/weaknesses as bars or bullet list. The teacher view might highlight things like “Weak Areas: Trigonometry, Punctuation; Strong Areas: Algebra, Data Analysis”.
- List of all assignments for that student and their status (completed, pending, score).
- Option to impersonate view as student or quickly jump to see exactly what the student sees (some systems allow teacher to “view as student” for support).
- A “Notes” section where teacher can write private comments (for themselves or other teachers/admins) about this student’s progress or needs.
- Possibly a log of AI tutor usage or study time to gauge effort (e.g., “Time spent last week: 3h 20m”).

**3. Assignment Creation Workflow:** A UI flow (likely a modal or separate page) for teachers to create assignments:

- **Step 1: Choose Type** – radio buttons or icons for “Full-length Test”, “Section Quiz”, “Custom Quiz”, “Homework (non-automated task)” etc.
- **Step 2: Configure Content** – if Full-length, choose from available test forms (or “Random new test”). If Custom Quiz, select subject(s), number of questions or manually pick questions:

  - A question picker interface: possibly show a list of questions (with filters by topic/difficulty) with checkboxes to add to quiz. Or after specifying criteria, the system selects and shows the chosen questions for review.
  - The teacher can preview each question (a dropdown to see the question text).
  - Alternatively, for speed, a teacher could say “Generate 10 questions on Grammar and Usage” – in which case the AI content generation is triggered and a spinner or progress indicator shows until ready. The new questions appear for confirmation.

- **Step 3: Assign to Students** – choose which class or select individuals. If the teacher came from a class context, that class is pre-selected. Could allow multiple classes or group selection if needed.
- **Step 4: Schedule** – set due date & time. Possibly time limit if it’s meant to be done in one sitting (though if it’s a full test, time is inherent). If it’s a homework like an essay, maybe no time limit but just due date.
- **Step 5: Instructions** – a field to add any additional note to students (e.g., “Complete this without calculator”).
- Finally, “Assign” button to confirm. After assigning, students get notified and the teacher returns to dashboard where the new assignment is listed.
- The UI for this should be wizard-like, guiding the teacher step by step. Use of modals or pages with clear “Next” and “Back” navigation.

**4. Analytics & Reports (Teacher):** Similar to student analytics but aggregated:

- A “Reports” tab where a teacher can select a report type (individual student report, class report, question item analysis).
- **Class Report:** Shows distribution of scores, average improvements, and perhaps can compare against past classes (if teacher has historical data). Could allow selecting two dates to see improvement over that period.
- **Item Analysis:** If a teacher views a particular assignment’s results, the UI might show question-by-question stats. For example, an assignment detail page: list each question, what percent got it right, which wrong answer was most common. Perhaps highlight if a majority picked a particular wrong answer (meaning a misconception). This might be shown in a color-coded way or with icons highlighting tricky questions.
- Ability to export these as PDF or CSV from the interface (e.g., “Export class results”).

**5. Content Management (for teachers who create content):** If teachers have access to create or suggest content (not all will, but possibly some):

- An interface similar to content manager’s view (described below) but maybe limited. They might be able to create a question that only their class uses (unpublished globally). The UI for that would be a form to input question, answer choices, etc.
- Or a simpler “feedback” mechanism: on any question’s explanation page, a teacher might see an “Suggest Edit” button to report an issue with content. That pops up a form to send to content managers.

Teachers’ UI focuses on oversight and easy management rather than doing the content themselves. It should minimize clicking through multiple screens; hence the dashboard consolidating info. Consistency with student UI is kept for things like how questions are displayed (so a teacher reviewing a question sees it in the same format a student would, just with the correct answer marked).

### Admin Interface

**1. Admin Dashboard (Organization Overview):** An admin (school admin or tutoring manager) sees top-level metrics:

- **User Statistics:** number of active students, number of teachers, perhaps license usage vs purchased.
- **Performance Summary:** maybe average score improvement across the organization, or distribution of scores if that’s of interest. If multiple schools or groups under admin, maybe comparisons or a list of top performing groups.
- **Recent Activity Feed:** e.g., “Teacher X created an assignment for Class Y” or “100 questions were practiced in the last 24h” – gives a pulse of platform usage.
- **Actions:** Quick links to manage users, classes, content, view reports. Possibly an “Invite Users” big button.

**2. User Management UI:** A section where admin can:

- See a list of all users (with filters by role, class, etc.).
- Click a user to edit their info or reset password, etc.
- Bulk actions: invite multiple students (maybe by uploading CSV or typing emails), create new teacher account, deactivate a user.
- Possibly manage roles: clicking a teacher might have a checkbox “Make this user also an Org Admin” or similar (with appropriate warnings).
- For privacy, certain fields might be hidden or editable only in certain ways (e.g., admin can change a student’s class but maybe not see their password – they’d send a reset link instead).

**3. Class Management:** Admins can create classes and assign a teacher to them (especially if setting up before teachers do).

- A form for class name, associated teacher, and optional list of students (or just instruct teacher to add, depending on workflow).
- Admin can see all classes and which teacher and how many students.
- Possibly override or archive classes (if a term ended, etc.).

**4. Content & Settings (Admin):**

- If the organization has some control over content, the admin might see a library of content (or at least what their teachers have created privately).
- They might also set organizational preferences: e.g., toggle features on/off (maybe “Enable AI tutor for students: yes/no” if, say, some school is concerned about AI and wants it disabled – the platform could allow that configuration at org level).
- Integration settings: for example, an “Integrations” page where admin can set up LMS LTI keys or SSO. This UI might involve forms to input the credentials or redirect to sign in to Google to connect.
- Subscription/billing info if applicable (or at least see when the license expires, number of seats, etc., though actual billing might be offline for enterprise deals).

**5. Reports (Admin):**

- More broad than teacher reports: e.g., compare multiple classes or aggregate for the whole school.
- Possibly filter by demographic if such data is input (if school tags students by grade or other categories).
- Downloadable summary that can be presented to school boards or executives – focusing on improvement and usage (e.g., “Our students answered 50,000 questions and improved average ACT by 4 points” in a given period).

Admin UI should be clean and somewhat utilitarian, with an emphasis on reliability and clarity. These users may be less frequent but need high-level control when they do log in. Use of tables and forms will be prevalent. Ensure confirmation dialogs for destructive actions (like removing a user or resetting data).

### Content Manager Interface

(If content managers are typically internal product team members, this interface might be less polished for end-users, but let’s assume it should still be user-friendly in case some educators use it.)

**1. Content Dashboard:** Shows status of the content repository:

- Counters of questions in the bank, by subject. “English: 1200 questions, Math: 1300, Reading:800, Science:900” etc.
- A queue or list of “Questions awaiting review” – e.g., 20 new AI-generated questions pending approval.
- Recent activity: who approved/edited what content recently (if multiple content curators).
- Possibly analytics on content usage (e.g., “Top 10 most answered questions” or “Questions with high error rate” as discussed).

**2. Question Review Screen:** When reviewing generated content:

- The question text and answers are displayed similarly as it would to a student.
- Below, the AI-provided explanation and any tags/difficulty classification.
- The content manager can edit any field: maybe they click on text to edit in place, or there’s an edit mode with input fields for each part.
- Buttons: “Approve”, “Send back for regen” (or “Reject”). Maybe “Improve” which would open an edit interface or allow them to tweak and then approve.
- If metadata needs editing: dropdowns or checkboxes to adjust tags (e.g., re-label a question as hard instead of medium).
- Navigation to jump to next question in queue easily.

**3. Content Editing/Creation:** To manually add content:

- A form very much like reviewing, but blank fields to fill in: question text (with a rich text editor in case of special formatting or math equations, possibly integrating a LaTeX editor for math), answer choices fields, correct answer selector, explanation field.
- Ability to attach an image if needed (e.g., upload an image if the question requires a diagram).
- Tagging interface to categorize the question.
- Possibly a “Generate with AI” helper inside this form: for instance, the manager could input “Need a geometry question on circles” and hit generate, and the AI fills in the fields which the manager can then refine. This accelerates manual content creation.
- Save or Save+Approve options.

**4. Test Form Management:** If the platform maintains specific full test forms (like a set of 10 official-like tests):

- An interface listing all test forms, which sections they contain, etc.
- Creating a new test form by selecting questions for each section. This could be done manually or via an auto-fill (“Generate full test” button that picks questions according to blueprint).
- Ensuring that each section meets ACT criteria (the interface can show counts of question types, etc., updating as content manager adds them).
- After building a test form, they can publish it so it becomes available for students/teachers to take.

**5. Content Library/Resources:** If including additional materials (lessons, videos, etc.):

- A library view listing all resources, with options to add new (upload file or link) and categorize.
- Possibly a rich text editor for creating “lesson pages” if we include that (not primary requirement, but could exist).
- Organize resources by topic or use-case (like a folder tree or tag cloud).

Content managers require a UI that is somewhat like an editor dashboard. It should prioritize accuracy and completeness (e.g., show all details of a question clearly). Since they might deal with lots of text, a clear typography and spacing is important. The design can be simpler and text-centric (less graphical fluff).

### General Design Notes:

- **Responsive Design:** All the above interfaces should be responsive. The student interface likely sees the most mobile use. For example, on mobile, the dashboard might turn into a single column of items (with a swipeable carousel for charts). The test interface on mobile might need a different layout (perhaps reading passage takes whole screen and you swipe to questions, or vice versa, which is challenging – likely we encourage full tests on larger screens, but ensure basic practice works on mobile).
- **Color and Branding:** The platform can use a neutral but modern color scheme. Possibly allow custom branding for enterprise (like school logos/colors via theming in the admin settings).
- **Icons and Visual Aids:** Use intuitive icons: e.g., a pie chart icon for analytics tab, a calendar icon for study plan, a clipboard for assignments, etc. These help users navigate quickly.
- **Tooltips and Help:** Small “?” icons or tooltips next to features that might need explanation (for example, a tooltip on the adaptive practice toggle saying “Adaptive mode adjusts question difficulty based on your answers”).
- **Feedback & Transitions:** Smooth transitions when moving between steps (like assignment creation wizard). Use modals for quick tasks (like confirming a deletion, or viewing one student’s data without leaving the page completely).
- **Error States:** Friendly error messages (e.g., if something fails to load: “We’re having trouble loading your assignments. Please refresh or try again later.”).
- **Loading Indicators:** Whenever data is processing (generating content, loading dashboard metrics), show spinners or progress bars so users know the system is working. For lengthy AI tasks, maybe an entertaining quote or tip about ACT could be shown to occupy the wait.
- **Testing and Iteration:** The wireframes should be user-tested with actual students/teachers if possible to ensure the design meets their expectations and is easy to use. Since product managers will use this document, they’ll ensure designers follow these guidelines and fill in the visual details accordingly.

In summary, the UI design is **user-centric**: students get an engaging, game-like learning environment; teachers get an efficient management console; admins have oversight tools; content creators have powerful editors. The wireframes and described elements ensure all major workflows are covered in an intuitive manner.

## Metrics for Success and KPIs

To evaluate the success of the platform and guide continuous improvement, we will track a variety of **Key Performance Indicators (KPIs)**. These metrics fall into several categories: user engagement, learning outcomes, content quality, and business outcomes. Below are the metrics and how we define success for each:

- **Student Engagement Metrics:**

  - **Active Users:** Number of daily active users (DAU) and monthly active users (MAU) on the platform. A growing or consistently high DAU/MAU indicates the platform is becoming a routine part of students’ study habits. We might aim for a certain percentage of registered users to be active weekly (WAU/MAU ratio).
  - **Session Length & Frequency:** Average time spent per study session and average sessions per week per student. For example, a goal might be each student spends at least 30 minutes, 3 times a week on the platform. If these numbers are low, it might indicate engagement issues or external factors limiting usage.
  - **Task Completion Rate:** The percentage of assigned study plan tasks or teacher assignments that students complete on time. Higher completion means students are following the guidance. If a lot of tasks remain incomplete, we investigate if tasks are too onerous or if reminder features need boosting.
  - **Retention Rate:** How many students continue using the platform over a period (e.g., from month to month, or across a school semester). A high retention suggests that once students onboard, they find sustained value. Churn (drop-off) rate should be low.
  - **Feature Usage:** Which features are used most. For instance, percentage of students who use the AI tutor chatbot at least once a week, or who take at least one full practice test in a month. If certain features (like full tests or study plans) are under-utilized, it may indicate a need for better onboarding or feature improvement.
  - **Engagement by Time:** We can see if there are peak usage times (e.g., platform usage spikes at 7-9pm) and ensure resources are allocated accordingly. Not exactly a success metric but helps in planning.

- **Learning Outcome Metrics:**

  - **Score Improvement:** This is a critical measure. We will track the average improvement in ACT practice scores from diagnostic to latest attempt for students who have used the platform for a defined period (e.g., 2 months or more). Success might be, for example, an average improvement of **+3 to +5 ACT composite points** after 8 weeks of use (this is just an example target; actual benchmarks will be informed by baseline data).
  - **Goal Achievement Rate:** The percentage of students who meet or exceed their target ACT score (or a more modest goal set by the system). If a student’s initial goal was 28 and they reach 28 or higher on a practice test, that’s a success mark. We’d compile how many achieved their goal by test day (if we get actual test results, or by last practice if not).
  - **Section Improvements:** We also monitor improvements per subject section to ensure balanced progress. For example, if most students improve in English and Reading but not in Science, that could indicate our science content or approach needs work. Ideally, we see improvements across all sections.
  - **Practice Efficacy:** Compare performance between those who use certain features versus those who don’t. E.g., students who followed their study plan 80%+ might have higher average improvement than those who didn’t – demonstrating the efficacy of that feature. If not, we analyze why.
  - **Diagnostic vs Final:** The platform could predict final scores; measuring the accuracy of our AI’s predictive analytics is also a metric (e.g., how close was the predicted readiness score to the actual ACT score for those who report back their official score).
  - **Content Mastery:** For each topic, track how many students move from “low proficiency” to “high proficiency” as they practice. If a large portion of users moved up levels in, say, algebra proficiency, that’s a positive learning outcome attributable to practice.

- **Content Generation & Quality Metrics:**

  - **Content Coverage:** Ensure we have sufficient content for all ACT areas. One metric is the number of quality questions per topic. For example, “at least 100 questions for each major subtopic of Math”. This is more of a product completeness metric.
  - **AI Generation Success Rate:** How often does the AI generate usable content on first pass? If content managers find that, say, 80% of AI-generated questions are approved with minor or no edits, that indicates high quality. If only 50% are usable and rest need heavy edits or rejection, we may need to improve the AI prompts or model.
  - **Content Refresh Rate:** How frequently new questions are added to the bank. This ensures returning students get fresh material. Perhaps target X new questions per month generated. A steady growth of the question bank is good.
  - **Error Reports:** Track the number of content errors reported by users (or found by internal review) – aim to minimize this. E.g., if teachers flag questions as incorrect and we get, say, <0.1% of questions flagged, that’s an acceptable quality level.
  - **Explanation Helpfulness:** Possibly measure via user feedback – e.g., after reading an explanation or using the AI tutor, the student can indicate if it was helpful. A high helpfulness rating (like average 4/5 stars or 80% “yes this helped”) means explanations are effective. If lower, need to refine explanation generation.

- **Platform Performance & Reliability Metrics:**

  - **Uptime Percentage:** We track uptime as a KPI (as agreed in NFR, e.g., 99.5% or above). This is important for client satisfaction (especially school admins). We aim to have no significant outages during critical usage times.
  - **Response Time Metrics:** Average and 95th percentile API response times. E.g., ensure 95% of question load requests happen in < 500ms. If this starts degrading as users grow, it triggers scaling or optimization.
  - **Error Rates:** Monitor error logs for spikes. E.g., any unhandled exceptions or failed API calls per thousand calls. Strive for error rate less than e.g. 0.1% of all requests.
  - While these aren’t success in the user sense, they are key for product health and indirectly user satisfaction. High performance and reliability contribute to positive user experience and thus usage.

- **User Satisfaction Metrics:**

  - **User Feedback & NPS:** Gather qualitative feedback. After a period of use, we might survey users: “How likely are you to recommend this to a friend?” to calculate a Net Promoter Score (NPS). A high NPS (e.g., 50+) would indicate users find significant value. We could also ask specific satisfaction questions about content, ease of use, etc.
  - **Reviews/Testimonials:** If the platform is sold to consumers or used by schools, their testimonials or renewal (for schools) is a metric. E.g., school renewal rate (if 90% of schools continue using next year, that indicates satisfaction and value).
  - **Support Tickets:** The number of support issues or questions raised by users. Ideally as the product matures, this number per user goes down (meaning it’s intuitive enough that they don’t need to ask for help often). A spike in certain types of tickets (e.g., “I can’t find X feature”) could indicate a UI problem to fix.

- **Business and Adoption Metrics:**

  - **Enrollment/Adoption Rate:** If the platform is licensed to institutions, track how many available seats or licenses are actually being used. Success is getting close to 100% utilization in each deployment. Or if available publicly, growth in user registrations over time.
  - **Conversion Rate:** If there’s a free trial or freemium aspect, measure conversion to paid subscriptions. For product managers, this indicates how well the product demonstrates value to get users to pay or commit.
  - **Cost per User and ROI:** On the business side, ensure that cost to serve each user (compute, support, etc.) is sustainable relative to revenue per user. This is more for internal business success, but product can impact it by being efficient (which ties to those performance metrics).
  - **Partnerships Integration Usage:** If we integrate with, say, an LMS, how many are using that integration (e.g., number of logins via Google Classroom)? If a large percentage of school-linked accounts use SSO, that’s good for user convenience, etc. Not a primary KPI but something to monitor to ensure we invest in the right integrations.

Product managers will regularly review these metrics. For example, a dashboard for internal monitoring might be set up to track these KPIs. We will define targets for key metrics in different phases:

- During initial pilot, focus on engagement (are students using it weekly, are they improving slightly).
- Over a longer term, focus on measurable score improvements and satisfaction (are teachers and students happy, do they credit the platform for score gains).
- For content, ensure continuous growth and coverage to handle repeat users.

By keeping an eye on these KPIs, we can iterate the product: if engagement is high but improvement low, perhaps add more instructional content; if improvement is great but engagement low (maybe only a few very dedicated students use it), figure out how to motivate broader usage (gamification, incentives, etc.). In essence, these metrics will validate if the platform effectively helps students prep for the ACT and inform any course-corrections in product strategy.

## Compliance with Educational Standards and Data Privacy

In developing and deploying the platform, we must ensure full compliance with relevant educational standards, ethical guidelines, and data protection regulations. This is critical both for legal reasons and for maintaining trust with schools, students, and parents.

### Alignment with Educational Standards

- **ACT Curriculum Standards:** All generated content (questions, tests, study recommendations) will align with the ACT’s official blueprint and College and Career Readiness Standards. This means:

  - The distribution of topics in generated full tests mirrors official ACT tests (e.g., the proportion of algebra vs. geometry questions, the types of reading passages, etc.).
  - Questions are phrased and formatted following ACT conventions (length of passages, style of answers, etc.). Explanations and strategies provided align with those a student would find useful for the ACT.
  - The difficulty calibration is tied to ACT score ranges. For example, easier questions correspond to those typically answered correctly by students in the low score ranges, whereas the hardest questions target top 10% scorers.

- **Common Core State Standards (CCSS) / Other Academic Standards:** While ACT is its own standard, many of its skills overlap with high school curricula. The platform can cross-reference Common Core (for Math and English) to ensure content isn’t outside the scope of what students have learned in school. For instance, ACT math doesn’t require calculus; we ensure no generated math question goes beyond Algebra 2/Trig as per ACT standards. Aligning with CCSS can help schools feel confident our content reinforces classroom learning rather than introducing completely foreign concepts.
- **Universal Design for Learning (UDL):** In content and UI, we adhere to principles that accommodate different learning styles. For instance, providing both written explanations and the ability to hear them (text-to-speech) addresses different needs. Study plans can be flexible (if a student needs a different approach, teacher can adjust), etc. This is more of a guideline to ensure accessibility in learning, complementing technical accessibility standards.
- **FERPA-compliant Educational Use:** On the platform, student performance data could be considered part of their educational record. We treat it with confidentiality akin to how a school would treat grades (see privacy below). Also, any learning interventions or analysis we do with the data is for educational benefit of the student, consistent with FERPA’s provisions for “legitimate educational interests”.

### Data Privacy and Security Compliance

- **FERPA (Family Educational Rights and Privacy Act):** For U.S. schools, FERPA is paramount. Our platform will:

  - Obtain necessary assurances in agreements that the school/university remains the owner of student data, and we are a “school official” processing data on their behalf for an educational purpose.
  - Not disclose personal student information or education records to unauthorized parties. Teachers and school admins can see their students’ data, but one student cannot see another’s, and outsiders see none. Even within the system, content managers or support staff see student data only as needed (with proper permission and logging).
  - Provide a way for schools or parents to request access to a student’s records on the platform and to delete or correct them if required. For example, if a parent of a minor student requests to see all their child’s data on the platform, we can export a report (scores, activities, personal info) for compliance.
  - Only retain student data as long as necessary. We might have a data retention policy (say, we retain data for X years after account inactivity unless the school requests deletion sooner).

- **COPPA (Children’s Online Privacy Protection Act):** COPPA applies to users under 13. Typically ACT prep targets older students (13+), but if the platform is used by, say, advanced 7th or 8th graders, we must comply:

  - For any user under 13, we ensure we have **verifiable parental consent** before collecting personal information. In a school context, schools might provide consent on behalf of parents via agreements.
  - The platform does not display targeted ads or any unrelated third-party tracking to students (especially minors). Data collected is solely for educational purposes (scores, responses, etc.).
  - We provide a clear children’s privacy notice if applicable, explaining what info is collected and how it’s used.

- **GDPR (General Data Protection Regulation) and other international laws:** If we have users in the EU or other regions:

  - We’ll implement GDPR principles like data minimization (only collect what we need – e.g., we might not need a student’s home address or phone for this service, so we won’t collect it unless required for an integration).
  - Obtain user consent for data processing where required (e.g., if a student signs up individually, have them agree to a privacy policy). For school contracts, ensure we have Data Processing Agreements in place.
  - Users (or their guardians) have the right to request data deletion (the “right to be forgotten”). We will have processes for account deletion that scrub personal data, while perhaps retaining anonymized performance metrics for aggregate analysis.
  - If any data is stored or transferred internationally, ensure compliance with transfer regulations (like Standard Contractual Clauses if EU data is stored on US servers, etc.).

- **California Consumer Privacy Act (CCPA):** Similar to GDPR for California residents. Even though educational data under FERPA might be exempt in some ways, we’ll largely treat it with similar care – giving transparency and control to the data subjects.
- **Data Security Standards:**

  - We aim for **SOC 2 compliance** in security (though SOC 2 is an auditing framework, not law, many edtech companies pursue it to assure clients of security practices). This covers security, availability, confidentiality of the system.
  - Regular security audits and penetration testing will be done. We keep software up-to-date to patch vulnerabilities (as noted in NFRs).
  - Encryption: All web traffic is HTTPS. Sensitive personal info (if any beyond names/emails) is encrypted at rest. Passwords are hashed with strong algorithms.
  - Access control internally: Only authorized staff can access the production database or files, and any access is logged. Admins at schools only see their school’s data – multi-tenant isolation is in place.

- **Student Data Privacy Pledges:** We may adhere to frameworks like the “Student Privacy Pledge” (endorsed by many edtech companies) which basically promise not to sell student data, not to use it for behavioral ad targeting, to use data only for educational purposes, to enforce strict limits on data retention, etc.
- **Content Moderation and Bias:** We must ensure the AI-generated content is appropriate:

  - No offensive or biased language in questions or explanations. Implement AI content filters and human review especially early on. For instance, avoid stereotypes in passages or questions. Ensure gender/racial/etc. representation in questions is fair and doesn’t introduce bias that could affect any group of students negatively.
  - If any user-generated content is allowed (for example, if teachers can input their own material or students can post in a forum if one existed), we’d need moderation policies. Currently, our main user-generated content is limited (possibly teacher-created questions or notes).

- **Accessibility (ADA):** Legally, software used in schools should be accessible to students with disabilities (Section 508 compliance in the US). As noted, we design for WCAG 2.1 AA. This means:

  - All interactive elements have labels for screen readers.
  - Videos have captions, images have alt text.
  - The web application can be navigated via keyboard (for those who cannot use mouse).
  - Colors used pass contrast checks, and there are settings or alternatives for color-blind users (e.g., not relying solely on color to convey correct/incorrect feedback).
  - We test with screen reader software to ensure a blind student could, for example, listen to a passage and questions and answer using just keyboard and screen reader cues.
  - Offer accommodations modes if needed (like adjustable timer for those with extra time accommodation – a compliance with disability accommodations).

- **Ethical AI Use:** Because we use AI heavily, we commit to ethical guidelines:

  - Be transparent (to an extent) with users that AI is used in generating content. For example, students and teachers should know that some questions are AI-generated and that we have quality control in place. If an error is found, we quickly correct it – this maintains trust.
  - The AI tutor should be monitored to not give wrong advice. We might log tutor conversations (anonymously) to identify if it ever gives incorrect or harmful guidance and retrain or adjust as needed.
  - Data used to train or prompt AI will not include personally identifiable student data. For instance, if we fine-tune a model on student answers to learn common mistakes, we would anonymize that data.
  - We avoid AI that evaluates students in high-stakes ways without human oversight (e.g., if we eventually have AI grade essays, we should let students/teachers know it’s an AI perspective and perhaps provide an option for human review).

### Policies and User Agreements

- We will have a clear **Terms of Service and Privacy Policy** that outlines all the above for end-users. It will explain what data we collect (e.g., name, email, performance data), how we use it (to provide and improve the service, to give feedback to the student and their educators), and how we protect it. It will also cover that we don’t sell data, and conditions under which we might share (only with their school, or if legally required, etc.).
- For schools, we sign agreements that include Data Privacy Addendums referencing FERPA, etc., as standard in contracts.
- Compliance with **CIPA** (Children’s Internet Protection Act) for schools: While CIPA mainly concerns filtering of obscene content on the internet in schools, our platform’s content will obviously be educational and vetted, and our web access is the platform itself (which is appropriate). We won’t link out to non-compliant sites. If we embed YouTube, we’ll use education mode or ensure no inappropriate content appears. Essentially, nothing on our site should trigger CIPA concerns, but we acknowledge and support schools’ filtering (e.g., make sure our domain is categorized correctly for school filters).

By adhering to these compliance requirements, we not only avoid legal issues but also build a platform that educators can trust. Many schools perform thorough vetting of software – having strong answers for how we handle student data, and demonstration of alignment to standards and accessibility, will be key to adoption. We will maintain documentation of our compliance efforts and be prepared to undergo security and privacy audits by districts or companies as needed.

---

**Conclusion:** This comprehensive document provides a full specification for the AI-driven ACT Prep SaaS platform. By following these requirements, product managers and the development team will be equipped to build a platform that is feature-rich (adaptive practice, AI-generated content, analytics), user-friendly (intuitive UI for all roles), technically robust (scalable, secure architecture), and compliant with the needs of the educational domain. The end result aims to be a transformative tool that not only makes ACT preparation more efficient and personalized through AI, but does so in a manner that earns the confidence of students, educators, and institutions alike.
