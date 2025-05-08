# ACT Exam Training SaaS Platform – Product Requirements Document

## Introduction

This document is a comprehensive Product Requirements Document (PRD) for a **Software-as-a-Service (SaaS) platform that trains students for the ACT exam**. It outlines all functional and non-functional specifications, structured by major modules. The intended audience is product managers and stakeholders responsible for planning and overseeing the development of the platform. The platform’s goal is to help high school students prepare for the ACT through realistic practice tests, rich learning content, personalized AI-driven tutoring, and robust progress tracking.

**Scope:** The platform will include a web application and a complementary mobile app, covering end-to-end user journeys from registration and practice to performance analytics. Key functional modules covered in this document are:

- Student Portal
- Practice Test Engine
- Learning Content System
- AI Tutor Integration
- Admin Dashboard
- Analytics and Reporting
- Notification System
- Payment and Subscription
- Mobile App Interface
- API Architecture for External Integrations

Each module section below details its purpose, features, user stories, use cases, UI/UX expectations, performance requirements, and security considerations. Cross-cutting requirements for security, privacy (FERPA/GDPR compliance), performance, scalability, and UI/UX principles are also addressed in dedicated sections.

**Out of Scope:** The PRD does not include low-level technical design, implementation details, or UI wireframes. It focuses on _what_ the system should do (requirements) rather than _how_ to build it. However, it does provide guidance on expected architecture and scalability strategies to meet performance goals.

### Goals and Objectives

- **Realistic ACT Practice:** Provide students with an environment to take full-length and sectional ACT practice tests under realistic conditions, with automatic scoring and feedback that mirrors the official ACT format.
- **Personalized Learning:** Offer a rich library of learning resources (videos, quizzes, notes) and an AI tutor that adapts to each student’s strengths and weaknesses, providing personalized feedback and study recommendations.
- **Progress Tracking:** Enable students to track their progress and improvement over time through dashboards and analytics, and enable educators or admins to monitor cohort performance for insights.
- **High Engagement:** Keep students engaged and motivated via an intuitive user experience, timely reminders/notifications, and possibly gamification elements (e.g. progress milestones, streaks).
- **Robust Administration:** Allow platform administrators (and optionally instructors) to manage content, users, and view analytics through a secure admin portal.
- **Scalability & Reliability:** Ensure the platform can scale to thousands of users with high availability, while maintaining fast performance and data security.
- **Compliance & Security:** Adhere to educational data privacy laws (FERPA) and general data protection regulations (GDPR), implementing strong security measures to protect student information and ensure trust in the platform.

## User Roles and Personas

To clarify the context of user stories and requirements, the platform will serve several types of users:

- **Student (Primary User):** A high school student preparing for the ACT. Needs access to practice tests, learning materials, AI tutoring, progress tracking, and personal study planning. This is the main end-user of the platform.
- **Administrator (Internal PM/Content Manager):** Platform administrators who manage content (questions, lessons), manage user accounts (including student accounts if needed), monitor usage, and ensure the system runs smoothly. They require an Admin Dashboard with full access to data and management tools.
- **Instructor/Teacher (Optional Role):** In some scenarios, an educator or tutor might use the platform to track a group of students (a “cohort”). They would need access to student analytics and perhaps the ability to assign tests or content. (This role can be considered a limited admin with access restricted to their students’ data.)
- **Parent/Guardian (Optional Future Role):** A parent who might pay for the subscription and wish to monitor their child’s progress. While not a core user in this initial scope, certain features (progress reports, payment management) may involve parents.

For the purposes of this document, **“admin”** refers primarily to internal product admins or content managers. **“User”** generally refers to students, unless otherwise specified.

## System Overview

The ACT Training SaaS platform is composed of multiple integrated modules, each handling a distinct set of functionalities, yet working together to deliver a seamless experience. Below is a high-level overview of how these modules interact:

- **Student Portal:** The entry point for students – handles user registration/login, profile management, and presents a dashboard that links to practice tests, learning content, AI tutor, etc. It aggregates information like test history and progress metrics for the student.
- **Practice Test Engine:** Manages the creation and delivery of ACT practice exams (full-length or section-specific). It times the sections according to ACT rules, presents questions, records answers, auto-grades the exam upon completion, and stores the results.
- **Learning Content System:** A library of instructional content – video lessons, practice quizzes, and textual notes or summaries. It is organized by ACT subject and topic. Students can consume this content on demand to learn concepts and strategies.
- **AI Tutor Integration:** An AI-powered chatbot and recommendation system that provides on-demand tutoring. It can answer students’ questions, explain solutions, and suggest study activities. It also analyzes student performance data to give adaptive learning recommendations.
- **Admin Dashboard:** A back-end interface for administrators to manage the platform. This includes managing user accounts, uploading or editing content, creating test forms, configuring notifications, and viewing high-level analytics. It ensures content and users are up-to-date and allows intervention when needed (e.g., resetting a password, removing inappropriate content).
- **Analytics and Reporting:** The data analysis component that gathers student performance data and usage data to produce meaningful reports. Students see personal analytics (e.g., score trends), while admins (or instructors) see cohort-level insights. These analytics drive both user-facing dashboards and internal decisions.
- **Notification System:** A service for sending emails, SMS messages, and in-app notifications triggered by events or schedules. It keeps users informed and engaged – from reminding a student to practice, to confirming a subscription payment, to alerting about new content.
- **Payment and Subscription Module:** Handles all e-commerce aspects – plan selection, secure payment processing, subscription management, and access control based on subscription status. It ensures only subscribed users (or those in trial) can access premium features, and automates billing and renewals.
- **Mobile App Interface:** A mobile application (iOS/Android) offering the core features of the platform in a phone-friendly format. It connects to the platform via APIs, enabling students to practice and learn on the go, with considerations for offline access and push notifications.
- **External API Integrations:** The platform exposes certain functions via APIs for integration with third-party systems (e.g., school LMS, or partner applications). This includes authentication, data retrieval (scores, content), and possibly webhooks for events. It ensures the platform can plug into broader ed-tech ecosystems securely.

All these components are built on a cloud-based architecture designed for **scalability, security, and high performance**, details of which are discussed in the “Performance & Scalability” section. The modules are modular but integrated – for example, the AI Tutor uses data from the Practice Test Engine and Learning Content System to personalize its responses, and the Notification System works across all modules (sending score reports, reminders, etc.).

---

The following sections detail each module’s requirements and considerations.

## Student Portal

The Student Portal is the main interface for students. It handles user onboarding (registration/login) and provides a personalized dashboard for each student. Through the portal, students access all other features: starting practice tests, viewing learning resources, chatting with the AI tutor, checking their progress, managing their profile, etc.

### Key Features and Functional Requirements

- **User Registration & Login:** Support account creation with email and password (and potentially OAuth login options like Google). Registration should include capturing basic info (name, email, age or graduation year) and verifying the email. Secure password handling (hashing) is required. If under 13, consider parental consent mechanism (COPPA compliance) – though most ACT takers are older.
- **Student Dashboard:** Upon login, the student sees a dashboard summarizing their status:

  - Upcoming ACT test date (if the student inputs it) and a countdown.
  - Latest practice test score and improvement since last test.
  - A visual progress tracker (e.g., a chart of scores over time for each section).
  - Quick links to resume studying: e.g., “Continue your Math practice” or recommended next activity (possibly provided by AI tutor logic).
  - Notifications or alerts (e.g., “You have one incomplete test” or “New video on Science section added”).

- **Profile Management:** Students can view and edit their profile info – name, email, password reset, profile picture (optional), graduation year, target ACT score, and test date. They can also set preferences such as notification preferences (e.g., opt in/out of SMS reminders).
- **Test History:** A section in the portal listing all practice tests the student has taken, with key details like date, scores per section, and composite score. Students can click an attempt to see the detailed results and review questions.
- **Progress Tracking:** In addition to test history, the portal provides progress metrics:

  - A chart or table of best scores in each ACT section and composite.
  - Score improvement over time (e.g., difference between first and latest attempt).
  - Possibly proficiency by topic (if the system tags questions by topic, it can show “Math: 70% correct on Algebra, 50% on Geometry”, etc.).
  - Time spent on platform (hours of study, number of questions answered).

- **Access to Other Modules:** The portal serves as a hub linking to the Practice Test Engine (e.g., “Take a New Test” button), Learning Content (browse lessons/quizzes), AI Tutor (open chat), and Analytics (detailed progress reports). These could be accessible via a navigation menu or dashboard widgets.
- **Study Plan (Optional/Future):** The system might generate a personalized study schedule (e.g., which days to take practice tests or complete lessons) based on the student’s test date. This would be displayed on the dashboard calendar or schedule view. (Even if not in initial scope, the design should allow adding such a feature.)
- **Logout and Security:** Allow users to log out, and automatically log out after inactivity. Implement session management securely (e.g., HTTP-only cookies or token). Possibly support “Remember me” login with care for security.

#### User Stories (Student Portal)

- _As a new user,_ I want to easily register an account so that I can start using the ACT prep platform.
- _As a registered student,_ I want to log in and see a dashboard with my progress and next steps so that I immediately know how I’m doing and what to do next.
- _As a student,_ I want to update my profile (email, password, etc.) so that my account information remains current and secure.
- _As a student,_ I want to record my target test date and score goal so that the system can personalize my study plan and send relevant reminders.
- _As a student,_ I want to view a history of all my practice tests and their scores so I can measure my improvement over time.
- _As a student,_ I want to see my progress in each ACT section (English, Math, Reading, Science) so I can identify which subjects I need to focus on.
- _As a returning user,_ I want the dashboard to suggest a logical next activity (e.g., “Complete a practice Reading section” if my Reading score is lowest) so that I have guidance in my study.
- _As a student concerned about privacy,_ I want to be able to delete my account (and data) if I choose to stop using the platform, so that I have control over my personal information (related to GDPR – see Security/Compliance).

#### Example Use Case: Student Registration and Dashboard Access

1. **Registration:** A new student visits the platform and clicks “Sign Up”. They fill a form with name, email, password, and graduation year. The system sends a verification email. The student verifies their email and the account becomes active. (If under 18, optionally the system might request a parent email for consent; if under 13, the system would require parental signup due to COPPA – this can be an extension of this use case.)
2. **Initial Profile Setup:** On first login, the student is prompted to enter a target ACT test date (optional) and target score. They are also shown a brief tour of the dashboard.
3. **Dashboard View:** The student dashboard loads, initially with default content (no progress yet if new). It might show “Welcome \[Name]! Let’s start by taking a diagnostic test or exploring the content.” The UI is clean with clearly labeled sections: “Practice Tests”, “Lessons & Quizzes”, “Your Progress”, “Ask AI Tutor”.
4. **Navigation:** The student clicks on “Practice Tests” from the dashboard or menu, which navigates to the Practice Test Engine module (detailed in the next section). After taking a test and getting results, they return to the dashboard.
5. **Updated Dashboard:** Now the dashboard’s progress tracking widgets update to show the new score. For example, “Latest ACT Score: 22 (English 20, Math 23, Reading 21, Science 24)” and maybe a message “Great start! Your baseline is 22. Your goal is 28 – let’s keep going.”
6. **Ongoing Use:** Each time the student logs in thereafter, the dashboard reflects their current status (improved scores, pending assignments, etc.) and provides quick access to continue their prep.

#### UI/UX Considerations

- The Student Portal should be intuitive and student-friendly. The dashboard should **surface the most important information first**, using visual elements like charts, progress bars, and icons to make data easy to scan.
- **Visual Design:** Use a clean layout with the platform’s branding (e.g., school-like yet modern). Perhaps have a motivational tone (welcome messages, tips).
- **Navigation:** A top menu or sidebar can provide access to major sections (Dashboard, Practice Tests, Lessons, Analytics, Profile, etc.). Ensure the navigation is consistent across pages.
- **Responsive Design:** The portal pages must be responsive to different screen sizes (desktops, tablets, and in-browser on mobile), although a dedicated mobile app exists. On smaller screens, the layout should stack neatly (e.g., menu might collapse).
- **Dashboard Widgets:** Key stats might be shown as cards (e.g., a card for each ACT section score, colored by performance, and a card for composite). Allow clicking these to drill into more detail in the Analytics section.
- **Feedback & Help:** Provide tooltips or info icons explaining elements (for example, “Composite Score: average of your section scores”). A help or FAQ link should be accessible (maybe connecting to AI tutor for help or documentation).
- **Personalization:** Greet the user by name. Possibly show an encouraging quote or tip of the day to keep motivation.
- **Consistency:** The look and feel of the portal should remain consistent when moving between modules – e.g., when the student goes to take a test or watch a video, it should still feel like the same product (common header or theme).
- **Accessibility:** Design with accessibility in mind – high contrast options, screen-reader friendly labels (ARIA tags), and keyboard navigability for those who might not use a mouse. This ensures students with disabilities can use the portal effectively.

#### Performance and Security (Student Portal)

- **Performance:** Loading the dashboard should be quick – ideally under 2 seconds for main content. This may involve caching recent progress data. The number of database queries on login should be minimized (e.g., fetch summary stats in one query if possible). The registration process should also be snappy, with immediate feedback on form validation (e.g., password strength, email format).
- The portal should be able to handle many simultaneous logins, especially on peak times (perhaps evenings or right after school). Design for at least a few thousand concurrent user sessions without slowdown.
- **Security:** Registration and login must occur over HTTPS. Store passwords securely (bcrypt or similar hashing, never in plain text). Implement measures against brute-force (e.g., rate-limit login attempts or use CAPTCHA after several failed tries).
- Use email verification to ensure accounts are real. Possibly implement optional two-factor authentication for added security (though not mandatory for students, but maybe for admin accounts).
- The profile data (name, email, test results) are sensitive personal data – ensure proper access control so one student cannot access another’s data. The session token or cookie should be secure and protected.
- Privacy setting: allow students to opt out of certain data uses – e.g., if data is used to train the AI recommendations, disclose and allow opting out (as required by personalization opt-out under FERPA best practices).
- Audit trail: It could be useful (for support/debugging) to log important account events (account created, last login time, etc.), but these logs must be secured and privacy-compliant.
- **Compliance:** During registration, present Terms of Service and Privacy Policy, and require explicit consent for data processing, in line with GDPR requirements. The portal should also provide a way for users to request their data or account deletion (this could be through contacting support or a built-in function), complying with GDPR’s right to access and erasure.

## Practice Test Engine

The Practice Test Engine is the heart of the ACT prep experience – it allows students to take simulated ACT exams. This module delivers full-length tests and section-specific tests, handles timing, records answers, auto-grades the questions, and provides score results along with answer explanations. It aims to replicate the official ACT testing experience as closely as possible to build student familiarity and endurance.

### Key Features and Functional Requirements

- **Full-Length ACT Tests:** The system will offer full-length practice exams consisting of the four mandatory sections (English, Math, Reading, Science) and an optional Writing section. Each section should follow official ACT format and timing:

  - English: 75 questions, 45 minutes
  - Math: 60 questions, 60 minutes
  - Reading: 40 questions, 35 minutes
  - Science: 40 questions, 35 minutes
  - Writing (optional essay): 1 prompt, 40 minutes
    These timings and question counts should be configurable but default to the official standard.

- **Section Practice:** Students may choose to take a single section (or a custom combination of sections) rather than a full test. For example, a student can practice only Math or do a Reading+Science combo. The engine should handle timing and grading for that subset accordingly.
- **Question Delivery:** Present questions one at a time (or with a passage and related questions together, as appropriate for Reading/Science). Students should be able to navigate within a section:

  - **Next/Previous:** move linearly through questions.
  - **Flagging:** mark questions for review to revisit if time permits.
  - **Navigation Palette:** optionally, a quick overview of question numbers indicating answered/unanswered/flagged status, allowing jumping to a specific question within the section.

- **Timing Management:** A visible timer counts down the remaining time for the current section. When time is up for a section:

  - The engine should automatically end that section’s answering period (prevent further answers) and move to the next section (or end the test if it was the last section).
  - Optionally, allow a grace period setting for practice (e.g., continue past time with a warning, but mark that the student exceeded time – this could be useful for learning mode, but default should mimic real exam strictly).

- **Pause/Resume:** For a full-length test, decide whether to allow pauses. In real ACT, once started you can’t pause except the short break after Math. For practice, the platform might allow a student to pause and resume later, _with a clear indication_ that this isn’t how the real test works. This is a design decision: perhaps allow pausing only between sections, or allow one pause per test in case of interruption. If paused, store the state (answers so far, time remaining) and let the student resume where they left off.
- **Answer Recording:** As the student answers each question, the system records their answer. This can be client-side (in memory) until submission, but it should also periodically autosave progress to the server (to prevent data loss on crash or logout).
- **Submission and Auto-Grading:** When the student finishes all sections or chooses to submit (and confirms), the engine should:

  - Immediately score the multiple-choice sections by comparing answers to the answer key.
  - Calculate raw scores (# correct in each section). Then convert raw scores to ACT scale scores (1–36) using the appropriate scoring tables. (Initially, we can use a fixed scale conversion or approximate; advanced version might have different score mappings per test form if needed).
  - Calculate the composite score (average of the four section scores, rounded to nearest whole number).
  - If the Writing section was taken, optionally integrate an essay scoring mechanism. (Perhaps use an AI to score the essay on a 2–12 scale or have the student self-grade with rubric; at minimum, record that an essay was done and allow manual scoring later.)
  - Store the results (raw and scaled scores, time taken, date, etc.) in the student’s history.

- **Results Feedback:** After grading, present the student with their results:

  - Overall scores (section scores and composite). For example: English 21, Math 23, Reading 20, Science 22, Composite 22.
  - Indicate percentile or benchmark if available (e.g., “22 = roughly 50th percentile” – not critical, but could be nice context).
  - **Answer Review:** The student should be able to review each question with the correct answer and their answer marked. Provide explanations for each question (especially if content team has written explanations or if AI can generate them). Explanations help learning: e.g., “The correct answer is B because…”.
  - For wrong answers, consider highlighting the specific mistake or providing tips (this can tie into AI tutor – e.g., a button “Ask AI why I got this wrong”).
  - If time was an issue (e.g., some unanswered questions due to running out of time), flag that in the feedback (e.g., “You left 5 questions blank in Reading due to time”).

- **Multiple Test Forms:** The platform should support a bank of ACT practice tests (e.g., Test 1, Test 2, etc.) as well as randomly generated quizzes:

  - There could be official-like predefined tests that mimic real exams (with fixed sets of questions).
  - Additionally, a “custom quiz” mode might allow the system to pull a set number of questions from specific topics for targeted practice (this might overlap with the Learning Content quizzes feature, but using the test engine interface).

- **Difficulty Adaptation (Advanced/Future):** Optionally, allow an adaptive practice mode where the question difficulty adapts based on performance (though the ACT is fixed-form, adaptive practice could be separate).
- **Accommodations Settings:** (Future consideration) Some students have extended time accommodations. The engine could allow an admin or instructor to set a longer timer for a particular student (e.g., time-and-a-half). Not in core requirements unless serving school accounts – but mention that timing could be made configurable for special cases.
- **Integrity (for formal use):** If the platform were used in a proctored environment, it might need a full-screen mode or prevent switching windows. For home practice, this isn’t enforceable, but we won’t focus on high-stakes proctoring since it’s practice.

#### User Stories (Practice Test Engine)

- _As a student,_ I want to take a **full-length ACT practice test** under timed conditions so that I can simulate the real exam and assess my performance.
- _As a student with limited time,_ I want to take a **single-section test** (e.g., just ACT Math) so that I can practice that subject without doing a full exam.
- _As a student,_ I want the test to **automatically score** itself and show me my score immediately after I finish, so I get instant feedback on how I did.
- _As a student,_ I want to **review each question** after I finish the test, seeing the correct answers and explanations, so that I can learn from my mistakes.
- _As a student,_ I want to **pause a test** if something urgent comes up, and resume it later, so that I don’t lose my progress (though I understand this won’t be allowed in a real ACT).
- _As a student,_ I want the interface to warn me when **time is almost up** (e.g., 5 minutes left in a section) so I can manage my time and attempt all questions.
- _As a student who skipped the optional essay,_ I want the system to simply skip the Writing section and finalize my test results without requiring an essay, so that I can choose whether to practice the essay or not.
- _As a student,_ I want to be able to **stop early and score** what I’ve done (for instance, submit the test before time if I have answered what I can) so that I get results without waiting unnecessarily.
- _As a student,_ I want to know which **questions I flagged** during the test while reviewing, so I can pay extra attention to those I was unsure about.
- _As an admin/content creator,_ I want to add new ACT test forms or questions to the question bank, so students have fresh material and can’t just memorize answers from repeating a single test (admin role covered later, but it relates to keeping test content robust).

#### Example Use Case: Full-Length Test Simulation and Review

**Scenario:** A student decides to take a full ACT practice test (all sections). They choose “Full Test #1” from the Practice section.

1. **Starting the Test:** The system displays instructions: “You are about to begin ACT Practice Test 1. It consists of English (45 min), Math (60 min), Reading (35 min), Science (35 min), and an optional Writing essay (40 min). Once you start, timing will run continuously. Good luck!” The student clicks “Start Test”.
2. **English Section:** The first question appears (with passage if applicable). A timer starts counting down from 45:00. The student answers questions, navigates freely within the English section. They flag two questions to revisit. When the timer hits 5:00 remaining, the timer or an indicator subtly alerts “5 minutes left”. The student completes English with 2 minutes to spare and clicks “Next Section”. (If they hadn’t, it would auto-advance at 0:00.)
3. **Math Section:** Timer 60:00 starts. The student works through 60 math questions. They cannot go back to English now. The interface maybe provides a calculator pop-up (if allowed – ACT allows calculators for Math; the system might either allow the student’s physical calculator or provide a basic one on-screen as an option). The student finishes or time elapses.
4. **Break (if implemented):** The ACT usually has a 10-minute break after Math. We can simulate this by showing a “Break” screen counting down 10 minutes, with a “Continue to Reading” button that becomes active after at least 10 minutes (or the student can choose to skip break early). For practice, we might allow skipping the break.
5. **Reading and Science Sections:** Similarly handled, each 35 minutes. For Reading, the UI might show a passage on the left and questions on the right (or passage above questions) for convenience. For Science, possibly show data/chart with questions.
6. **Optional Writing Section:** After Science, the platform asks “Do you want to attempt the optional Writing essay?” If yes, it presents an essay prompt and a text box with 40:00 timer. The student writes their essay and submits, or skips if they choose not to do it.
7. **Submission:** Upon completing the last section, the test is submitted. The system immediately begins grading. A loading indicator may appear for a couple of seconds with a message like “Grading your test…”.
8. **Score Results:** The student is then shown a **Results Summary**:

   - English: 65/75 correct = Score 25 (for example).
   - Math: 50/60 correct = Score 28.
   - Reading: 30/40 correct = Score 26.
   - Science: 32/40 correct = Score 27.
   - Composite Score: 26 (the average of the four, rounded).
   - Writing (if taken): e.g., “Score: 8/12” (and possibly some feedback if AI scored it).
   - Perhaps a note about percentile (“Composite 26 \~ 83rd percentile nationally”) – optional informational.

9. **Review:** The student clicks “Review Answers”. The interface shows each section’s questions. For each question:

   - The student’s answer (marked incorrect if wrong).
   - The correct answer with explanation. For example, “Q5: Correct answer is B. **Explanation:** B is correct because ...”.
   - If the student flagged a question, highlight it or list flagged questions for quick access.
   - The student can navigate question by question or jump via a list.
   - The review mode is not timed; the student can take their time to understand mistakes. They might also see aggregate info per section, like “English: you answered 10 questions incorrectly. Topics missed: Punctuation (4), Grammar (3), Rhetoric (3).” if such tagging exists.
   - Option to **ask the AI tutor** about a question: e.g., a button “Ask Tutor” could send the question context to the AI chatbot for further clarification if the explanation isn’t clear.

10. **Completion:** The test results are saved in the student’s history. The platform might prompt: “Great work! What do you want to do next? \[Review mistakes later] \[Go to Dashboard] \[Recommend content based on this test]”. The student goes back to the dashboard, which is now updated with this new score data.

#### UI/UX Considerations

- **Exam-like Interface:** The test-taking UI should minimize distractions and mimic a real test booklet/screen. Likely a clean white background for questions, large readable text, and simple radio buttons or bubbles for answers. A progress indicator (e.g., “Question 15 of 75”) and a timer at top.
- **Timer Design:** The countdown timer should be visible but not alarming. Perhaps black text that turns red in the last 5 minutes. Optionally allow the student to hide the timer if it causes anxiety, as some prefer (this could be a toggle).
- **Navigation Controls:** Next/Prev buttons should be clearly visible. If a student tries to move to next without answering, we might allow it (since skipping is okay) but maybe mark the question as unanswered. A “Review” panel or button that lists all question numbers with their status (answered/blank/flagged) at a glance can help students manage time.
- **Flagging:** Include a flag icon or checkbox on each question to mark for review. In the review panel, flagged questions could have a special highlight.
- **Content Display:** For Reading and Science, which involve passages or data:

  - Use a split view or tab system so students can easily see the passage while answering related questions.
  - Possibly allow scrolling the passage independently.
  - Ensure any figures (charts in science, etc.) are clear and can be enlarged if needed.

- **Answer Input:** Multiple-choice can be a list of options labeled A, B, C, D (and E for 5-option Math). The student should be able to select an option easily (click or tap). We might allow keyboard shortcuts (like pressing A, B, C, etc., to select answer) for power users.
- **Submission Confirmation:** If a student hits “End test” or after the last question, confirm they really want to submit (especially if time is still remaining). “Are you sure you want to end the test and grade it now? You still have 5:30 minutes left in this section.”
- **Responsive**: On smaller screens (if someone uses mobile web or small tablet), the test UI should adapt (though ideally they’d use the mobile app for phone). Ensure buttons aren’t too small to tap.
- **Accessibility:** Provide ways to increase font size for questions/passage. Ensure screen readers can read the question text and options (though taking a timed test with screen reader might require accommodation of extended time).
- **Explanations UI:** In review mode, show explanations maybe collapsed under each question that can be expanded, to avoid overwhelming with text. Or show them directly under each question – but ensure it’s visually clear what the explanation is vs. the question text.
- **Visual Feedback:** Use color or icons to show correct vs incorrect: e.g., student’s chosen option marked with a red X if wrong, and the correct answer marked with a green check.
- **Saving State:** If the student disconnects or closes the browser accidentally, we should attempt to save test state so they can resume (perhaps via an auto-save every minute or at least at section boundaries). This is more of a back-end requirement but critical for UX – nothing worse than losing 30 minutes of answers.
- **Prevent Cheating (light):** While we can’t stop a student from looking up answers during practice, the UI should at least not show correct answers until after submission. Also, we might disable the ability to copy text from the question (to prevent easy googling) – though that’s not foolproof. It’s a fine line, but since this is practice, the main thing is the student hurting their own practice if they cheat.
- **Load Handling:** The question content (text/images) should ideally preload for the section to avoid delay between questions. If images (like science charts) are used, ensure they load quickly (use optimized images or embed in the content).

#### Performance Requirements

- The test engine must **not lag** during use. Transitioning to the next question or bringing up a passage should be instantaneous. All questions for a section could be loaded at start of that section to facilitate this.
- Timing accuracy is crucial; the timer should not drift. Use client-side timer for responsiveness, but also periodically sync with server to handle cases like the user trying to cheat by altering local time (the server should be authoritative on end time).
- **Concurrent Usage:** The system should handle many students taking tests simultaneously, especially on weekends or evenings. Grading is computationally light (mostly lookup) so that’s fine, but delivering content should be scalable (maybe use CDN for static content like images).
- If we assume, say, 1000 students start a test at roughly the same time (perhaps a class or popular study time), the system should manage that. Auto-save pings from 1000 tests per minute should not overload the server – use a lightweight mechanism or batch.
- **Auto-Scaling:** If a surge of test-taking happens (e.g., day before a real ACT, lots of practice), the module’s service should auto-scale. The stateless nature of delivering questions allows horizontal scaling (multiple servers can serve different users).
- **Data Volume:** Each test attempt is a lot of data (answers for 216+ questions including essay text). Ensure the database can handle continuous inserts of results. Possibly use a separate results logging service to not impact live user experience.
- The scoring algorithm (score conversion) should be optimized (it’s trivial math, so no issue).
- **Browser Performance:** The front-end should be optimized so even on a moderately powerful computer (or school Chromebook), the test UI runs smoothly without heavy scripts causing lag.

#### Security and Data Integrity

- **Content Security:** ACT questions are copyrighted. The system must ensure questions are not easily downloadable in bulk by unauthorized parties. This means:

  - Only serve question data to authenticated users actively taking a test.
  - Potentially watermark or uniquely tag content to deter sharing (though that might be extreme; a simpler approach is just limiting access).
  - Do not expose the entire answer key or test content via an insecure API. For example, the front-end shouldn’t fetch the whole test with answers in one go. It should fetch questions incrementally or without answers, and only fetch the key at submission server-side.

- **Answer Security:** While taking a test, answers should be stored securely. If temporarily stored client-side, use encryption if feasible or at least obfuscation. However, periodic server saves are safer.
- **Integrity:** Prevent tampering with results – e.g., a malicious user trying to submit answers via API bypass to get a perfect score. Mitigate by verifying that the answers came through the proper test-taking flow (maybe use session tokens, and definitely do scoring on server side).
- **Privacy:** The test results are part of student’s personal educational record. Only that student (and authorized teacher/admin) should see them. Ensure when fetching results, proper authorization checks are in place (e.g., user A cannot request user B’s results via manipulating an ID).
- **Cheating Prevention (if needed for proctored use):** This can include disabling copy/paste during test, or full-screen mode detection (if not in full-screen, warn the user). However, for unproctored practice, these are optional. Perhaps implement gentle measures (like a warning if they leave the test tab).
- **Data Loss Prevention:** If a server crash occurs, ensure that partial results are not lost. A robust approach: log responses as they’re entered (with minimal overhead). At least, if a test is submitted and the response processing fails, allow the attempt to be recoverable or not counted rather than vanish.
- **Load Testing:** Before release, simulate large numbers of concurrent test-takers to ensure the engine scales without timing issues or crashes. This is part of performance but critical to reliability.
- **Updates:** If content is updated (like a typo fix in a question) while a student is in a test, decide how to handle. Possibly lock test forms during active use or version them. Minor point but ensures consistency (not likely a frequent issue).

## Learning Content System

The Learning Content System provides the **instructional and practice materials outside of full exams**. This includes video lessons, practice quizzes (short sets of questions), and written notes or articles. It serves as a self-study library where students can learn concepts, review strategies, and reinforce skills in specific areas of the ACT.

### Key Features and Functional Requirements

- **Content Catalog:** Organize content by subject and topic. For example:

  - **English:** Topics like Grammar, Punctuation, Rhetorical Skills.
  - **Math:** Topics like Algebra, Geometry, Trigonometry, Word Problems.
  - **Reading:** Strategies for passages, identifying main ideas, etc.
  - **Science:** Interpreting graphs, Scientific investigation, etc.
  - **Test Strategies:** General sections on time management, guessing strategies, anxiety reduction, etc.
    Each topic may have multiple content items (videos, text, quizzes).

- **Video Lessons:** The platform will host (or embed) video lectures/tutorials. Requirements:

  - Videos should stream smoothly. Support common formats (MP4, etc.) possibly via a third-party video hosting (YouTube private links or a Vimeo, or cloud storage with streaming).
  - Track user’s progress in the video: mark as “watched” if completed. Optionally show a progress bar for partially watched videos so they can resume.
  - Duration display, the ability to pause/play, seek, and adjust volume. Perhaps speed control (0.5x to 2x) as students often like to speed up review or slow down for complex parts.
  - Closed captions or transcript for accessibility (highly desirable to meet accessibility requirements and for users who prefer reading along).

- **Interactive Quizzes:** Short quizzes associated with lessons or topics:

  - For instance, after a video about Algebra, a 10-question quiz to test understanding.
  - Quiz questions format: likely multiple-choice like ACT, but could also include a variety of forms (maybe fill-in for formula, though multiple-choice keeps it consistent).
  - Instant feedback mode: since these are practice drills, when a student answers a quiz question, the system can immediately tell them correct or incorrect and provide an explanation _without_ waiting until the end (unlike the full test which gives feedback only after completion). Alternatively, allow the quiz to be taken like a mini-test and then reviewed after submission – but immediate feedback is often more instructional in this context.
  - Record the quiz score for the student’s reference, but quiz performance may or may not count in their “official” progress analytics (likely it does, but with less weight than full tests).
  - Allow multiple attempts on quizzes, perhaps with question variations if available (e.g., a quiz could draw from a question bank so it’s slightly different each attempt).

- **Textual Lessons/Notes:** Not everything is video. Provide written content such as:

  - Summaries of grammar rules, math formulas, vocabulary tips, etc.
  - Articles on strategies (like how to read faster, how to analyze science passages).
  - Possibly downloadable PDFs or cheat sheets (e.g., “Common Math Formulas for the ACT”).
  - These should be viewable in the portal with proper formatting (headings, bullet points, perhaps images or examples).
  - Students should be able to highlight or take notes (see next point).

- **Student Note-Taking:** Allow students to take personal notes:

  - Possibly implement a notes section per lesson or a general notes tool. For example, on a video page, have a “Your Notes” textbox where they can jot things down while watching.
  - Save these notes to the user’s account (maybe tied to that lesson or globally). The student can review their notes later in a “My Notes” area.
  - Alternatively or additionally, allow bookmarking content (e.g., “bookmark this video or article” to easily find later).

- **Search and Filter:** A search bar to find content by keywords (e.g., “comma splice” brings up English lesson on comma usage). Filter content by subject, type (video/text/quiz), or difficulty level if applicable.
- **Progress and Completion Tracking:** Indicate which lessons have been completed:

  - Perhaps a checkbox or checkmark appears on content tiles when done.
  - Track quiz completion and scores.
  - Possibly unlock advanced content after basics are done (if a structured course flow is desired, though it could remain open so students can jump around).

- **Recommendations:** Tie in with AI/personalization:

  - For instance, after a student does poorly in a certain quiz or test section, the system (or AI tutor) can recommend “Watch these videos to improve”.
  - The content system might generate a dynamic “Recommended for you” list based on the student’s weaknesses (e.g., if Reading score is low, recommend “Strategies for ACT Reading” video).

- **Content Updates (Admin Side):** Admins need to be able to upload new content easily (will be detailed in Admin Dashboard section). The system should support adding new videos, editing text, and creating quizzes without code changes.

#### User Stories (Learning Content System)

- _As a student,_ I want to browse a **library of video lessons** for each section of the ACT so that I can learn or review content areas at my own pace.
- _As a student,_ I want to take **short quizzes after a lesson** to make sure I understood the material, and get immediate feedback on my answers so I learn from mistakes on the spot.
- _As a student,_ I want to read **written notes and tips** on specific topics (like grammar rules or math formulas) so I can quickly reference important information without watching a full video.
- _As a student,_ I want to be able to **search** for a topic I’m struggling with (e.g., “trigonometry”) so that I can quickly find resources that help me with that topic.
- _As a student,_ I want to **bookmark or save** certain lessons or questions that I found difficult, so I can easily revisit them later for review.
- _As a student,_ I want to **track which lessons or quizzes I’ve completed**, so I have a sense of progress in the content library and know what I have left to cover.
- _As a student,_ I want the system to **suggest what content to study** based on my weaknesses (for example, recommend a video on comma usage if I frequently miss comma questions) so that I can focus on improving my weak areas.
- _As a student,_ I want to **take notes** while studying (on videos or readings) and save them on the platform so that all my study notes are in one place and I can review them later.
- _As an admin/content creator,_ I want to organize content into a logical structure (subjects → topics → lessons) so that students can easily navigate through the curriculum.

#### Example Use Case: Using a Video Lesson and Quiz

1. **Browsing Content:** The student navigates to the “Learning” or “Lessons” section from the portal. They see categories (English, Math, Reading, Science, Strategies). The student selects **Math**.
2. **Topic List:** Under Math, they see a list of topics: e.g., “Algebra Basics”, “Geometry”, “Trigonometry”, etc., each perhaps with a progress indicator (0/3 lessons completed). The student chooses **Geometry** because they struggled with geometry questions on their last practice test.
3. **Lesson Selection:** Under Geometry, suppose there are multiple items:

   - A video lesson titled “Geometry Fundamentals: Lines and Angles” (10 minutes).
   - A video “Common Geometry Problems on the ACT” (8 minutes).
   - A text lesson “Geometry Formulas Cheat Sheet”.
   - A quiz “Geometry Practice Quiz – 5 questions”.
     These might be listed in a recommended order. The student starts with the first video.

4. **Watching Video:** The video player opens (taking the main area of the screen). It shows the title “Geometry Fundamentals: Lines and Angles”. The student clicks play. As the video plays, the student can pause if needed, use the timeline to seek back 10 seconds to re-listen to something, or turn on closed captions to read along. They take some notes in a “Notes” panel on the side (for example, they type “Remember: vertical angles are equal.”). The video is 10 minutes; the student watches fully. At the end, the system marks this video as completed (could show a checkmark). Their notes are auto-saved attached to this video.
5. **Taking Quiz:** After the video, the student clicks on the “Geometry Practice Quiz”. A short quiz interface appears with 5 multiple-choice geometry questions. The quiz might be untimed or lightly timed (maybe show time taken but no pressure). The student answers Question 1 and hits “Submit” for that question – the system immediately indicates “Correct!” with a brief explanation. For Question 2, they submit and it says “Incorrect – The correct answer is C. Explanation: …” explaining the concept. The student proceeds through all 5 questions this way, getting immediate right/wrong feedback each time.
6. **Quiz Results:** After the last question, a summary might say “You got 3/5 correct on the Geometry Practice Quiz.” It might highlight which questions were wrong and allow reviewing the explanations again. The system records this score in the background (for the student’s own analytics).
7. **Adaptive Suggestion:** Based on the quiz performance, the system or AI might prompt: “It looks like you struggled with Circle questions. We recommend the lesson ‘Circle Geometry’ next.” The student sees a suggestion to watch another video or read a note covering that subtopic.
8. **Continuing Study:** The student proceeds to either follow the recommendation or pick another item in Geometry. Suppose they open the “Geometry Formulas Cheat Sheet”. It’s a one-page written lesson listing area, perimeter, volume formulas, etc., possibly with diagrams. They read it and maybe print it or save it as PDF (if allowed).
9. **Completion and Tracking:** The Geometry topic now shows maybe 2/4 items completed (the video and the quiz). The student’s dashboard might reflect the time spent or number of lessons done. The student can always come back later; the system will remember where they left off (e.g., which videos watched).
10. **Later Review:** The student can go to a “My Notes” section to review the notes they wrote (like the note about vertical angles). They can edit or add to it after maybe doing more practice.

Throughout this, the learning content system complements the practice tests by building knowledge in specific areas.

#### UI/UX Considerations

- **Content Library UI:** This should feel like a course catalog or a learning management interface:

  - Possibly use cards or list items for each lesson with icons indicating type (video ▶️, quiz ❓, article 📄).
  - Show duration for videos, estimated time or number of questions for quizzes.
  - Maybe allow sorting by difficulty or marked as “recommended”.

- **Topic Navigation:** Breadcrumbs or a sidebar can help navigate (e.g., Math > Geometry > \[lessons list]). Students should easily jump to another topic or subject.
- **Progress Indicators:** Use visual cues for completed items (checkmark, different color). Maybe a progress percentage per topic (“50% complete”). This gives a sense of accomplishment and direction.
- **Inline Media:** The text lessons might include images or diagrams. Ensure these display well (zoomable if needed). All media should have alt text for accessibility (especially important for diagrams explaining concepts).
- **Quiz UI:** For lesson quizzes, since they are learning-oriented, you might show the explanation right after each question (as described). Alternatively, could do at end – but immediate feedback is usually better for learning. This is distinct from the full test engine where we delay feedback to simulate test conditions.
- If immediate feedback is used, design it clearly:

  - Show a green highlight for correct, red for incorrect, along with a short text explanation. Possibly also link to the related content (e.g., if got a geometry question wrong, link “Review Geometry Fundamentals video”).
  - Allow the student to retry the question or similar questions if possible.

- **Responsiveness:** Content pages and quizzes should work on mobile sizes as well, as students might use these on their phones (especially videos). The layout should reflow nicely (e.g., list of lessons becomes a single column list).
- **Download Options:** For textual content or notes, might allow “Download PDF” for offline study or printing. Videos, if hosted, maybe not direct download, but could allow offline in the mobile app.
- **Note-Taking UI:** If we have in-app note capability, ensure it’s always accessible but not intrusive. Perhaps a “Take Notes” button that opens a sidebar or popup with a text area. Or a simple text area below the video. Save automatically as they type (so they don’t lose notes if they navigate away).
- **Notifications within Content:** If the student completes all lessons in a topic, maybe show a congratulatory message or badge (“Master of Algebra!”).
- Possibly incorporate **gamification**: e.g., earn points or badges for completing lessons or quizzes, to motivate usage. (This wasn’t explicitly asked, but it’s a UI/UX idea that PMs might consider to drive engagement.)
- **Search Functionality:** The search bar should be prominent on the content library page. It should search through titles, descriptions, and maybe even transcript text of videos (if available) to find relevant content. Show results with context (like “found in Math > Geometry: Lesson X”).
- **Consistency:** The style of content pages should match the overall app but can be slightly more content-focused (like an educational site). Use the same header/footer so navigation back to dashboard or other sections is easy.

#### Performance and Security

- **Content Delivery Performance:** Videos should be delivered via a streaming service or CDN for smooth playback without buffering on normal internet connections. We should support adaptive bitrate streaming if possible, so users on slower connections get a lower quality stream rather than constant buffering.
- For text and images, use caching so that frequently accessed content (like popular lessons) loads quickly. Perhaps preload certain assets when a student enters a topic.
- The search function should be indexed to return results quickly (perhaps use a search engine or at least database full-text indexing).
- **Concurrent Use:** Many users might watch videos simultaneously – ensure the video hosting can scale (cloud bandwidth or using something like YouTube unlisted for small scale, or a professional video CDN for larger scale).
- **Security (Content):** Ensure that premium content (videos, etc.) is accessible only to authorized users (i.e., those logged in, and with subscription if required).

  - For example, video URLs should be protected (expiring URLs or embedded players that require auth token). We don’t want someone to simply copy a link and share all the lessons publicly.
  - Text content should likewise require login to view.

- **Intellectual Property:** The content likely is proprietary (videos made by the company, question bank, etc.) Protect it from piracy as feasible (though completely preventing screen capture or manual copying is impossible, we can deter casual theft).
- **Data Tracking:** Track usage of content (views, completions) as this feeds into analytics and personalization. Also track quiz responses to feed the AI tutor or recommendations.
- **Crash/Error Handling:** If a video fails to load (network issue), app should handle gracefully (retry or prompt user). If a quiz submission fails due to disconnect, allow retry and ensure no duplicate grading issues.
- **Updates:** When admins update content (like fix a typo in notes or add a new question to a quiz), ensure consistency: e.g., if a student is in the middle of that quiz, how to handle? Ideally, content changes wouldn’t affect in-progress sessions – this likely isn’t a big problem for short lessons though.
- **Integration:** The content system might integrate with the AI tutor – e.g., the AI might point to specific lessons. So maintain a consistent ID or tagging for content so AI or other modules can reference them reliably (for instance, tag lessons by topic for AI to suggest “topic X materials”).

## AI Tutor Integration

The AI Tutor is an intelligent virtual tutor embedded in the platform. It leverages artificial intelligence (likely natural language processing and machine learning on student data) to provide personalized, interactive assistance. The AI Tutor functions both as a **chatbot** that students can converse with and as an **adaptive engine** that tailors the learning experience to each student. This module is a key differentiator, offering on-demand tutoring and feedback beyond static content.

### Key Features and Functional Requirements

- **Chatbot Interface:** Students can enter a chat with the AI tutor, asking questions in natural language. This could be a general “Ask me anything about the ACT” assistant. Capabilities include:

  - Answering questions about ACT content (“What’s the formula for the area of a circle?”), test strategies (“How should I manage my time on Reading?”), or even specific practice questions (“I didn’t understand question 5 on that quiz, can you explain it?”).
  - Providing step-by-step solutions to problems the student inputs, similar to how a human tutor would work through an example.
  - Explaining why an answer is correct or incorrect, or clarifying concepts the student finds confusing.

- **Contextual Awareness:** The AI should utilize context when possible:

  - It knows the student’s recent activity (e.g., which practice test they just took, or which question they got wrong) and can tailor its feedback accordingly: “I see you struggled with the last math question on geometry; let’s go through it.” It might fetch the exact question if needed or at least know the topic.
  - When accessed from a particular screen, it might pre-load context. For example, if a student is reviewing a test question and clicks “Ask AI”, the AI is fed the question and the student’s answer to provide an explanation.

- **Personalized Feedback and Recommendations:** Beyond Q\&A, the AI tutor acts as a mentor:

  - After each practice test, the AI could generate a personalized analysis in a conversational format: “Hi! I’ve reviewed your results. Great job improving your Math score. It looks like comma usage in English and science reasoning questions gave you trouble. I suggest focusing on those. Shall we practice some comma questions now?”
  - The AI can recommend specific lessons or quizzes: “Based on your performance, I recommend watching the ‘Comma Rules’ video and then trying a few practice questions. I can generate some for you or you can find them in the English section.”
  - Adaptive practice: The AI can create a mini-quiz on the fly focusing on the student’s weak areas (drawing from the question bank). _Example:_ “Sure, I’ve compiled 5 practice questions on punctuation. Let’s do them one by one.” It then goes through them in the chat, essentially acting as an interactive quizmaster.

- **24/7 Availability:** The tutor is always available for help, unlike human tutors with schedules. Students can use it late at night or whenever.
- **Natural Language Understanding:** The AI should handle a range of inputs:

  - Direct questions (“How do I solve this equation: 2x + 3 = 7?”).
  - Expressions of confusion (“I don’t get why my answer was wrong.”).
  - Broad guidance requests (“What should I study next?”).
  - Motivation or strategy queries (“Any tips to stay focused?”).

- **Tone and Persona:** The AI should have a friendly, encouraging persona. Professional but approachable, as if a knowledgeable tutor. It should praise progress (“Great, you got it right!”) and encourage (“No worries, many students find this hard. Let’s break it down.”).
- **Learning and Adaptation:** Ideally, the AI improves with use:

  - It “learns” about the student’s learning style or patterns over time (e.g., notices they prefer detailed explanations vs. brief, or that they repeatedly ask about certain topics).
  - It might adjust its explanations accordingly (for instance, if a student always asks for another example, the AI proactively provides examples).
  - This could be achieved by tracking interactions and outcomes (if the student says “That helped” vs “I’m still confused,” etc., the AI adjusts its approach).

- **Integration with Human Support (Optional):** Not for initial release, but consider if AI cannot handle a query, it might suggest scheduling a session with a human tutor or refer to an FAQ. Or allow admins to review AI interactions to correct any misinformation.
- **Safety and Accuracy:** Ensure the AI provides accurate academic help:

  - Use a knowledge base or training that includes ACT curriculum, official explanations, etc., so it doesn’t hallucinate incorrect info.
  - All answers and explanations ideally should be verified or come from human-vetted sources (Juni’s Acely example ensures content is human-verified for accuracy).
  - Content moderation: If a student asks something off-topic or inappropriate, the AI should handle gracefully (either politely say it’s not relevant or comply with safety guidelines not to produce harmful content).
  - The AI should avoid giving outright the answer to a current test question without explanation. Instead, guide the student to understand (to prevent just cheating through AI).

- **Technical Implementation Note:** Likely this involves integration with an AI service (like OpenAI GPT or a similar model) plus a custom layer with context injection (student data, question bank info) and guardrails. We need to manage cost (calls to AI API) and latency (aim for responses in a couple seconds).

#### User Stories (AI Tutor)

- _As a student,_ I want to **ask the AI tutor questions** any time I’m stuck on a problem or concept so that I can get help right away instead of waiting for a teacher.
- _As a student,_ I want the AI tutor to **explain solutions step-by-step** for a problem I don’t understand, so I can learn how to solve it on my own next time.
- _As a student,_ I want the AI tutor to **give me personalized recommendations** on what to study next based on my performance, so I focus on improving my weaknesses.
- _As a student,_ I want the AI tutor to **adapt** to my needs – for example, if I keep getting a type of question wrong, it should offer to practice that type more, so my practice is tailored to me.
- _As a student,_ I sometimes feel discouraged; I want the AI tutor to **encourage and motivate** me (celebrate improvements, reassure when I mess up) so I stay positive about my prep.
- _As a student,_ I want to be able to **have a conversation** with the AI, not just isolated Q\&A – for example, I might ask a follow-up question if I don’t get the explanation, and the AI should handle that context.
- _As a cautious student,_ I want to be sure the AI’s advice is **trustworthy and accurate**, so I can rely on it without being misled (this implies I want to know that the platform has verified the AI’s content or there’s oversight).
- _As an admin,_ I want to **monitor AI interactions** (at least in aggregate or with consents) to see common questions and ensure the AI is providing correct info, so that we maintain quality and can update its knowledge base if needed.

#### Example Use Case: Interactive Tutoring Session

**Scenario:** A student just reviewed a practice test and saw they struggled with a particular math question. They decide to use the AI Tutor for help.

1. **Starting Chat:** The student clicks on the “AI Tutor” chat icon (possibly accessible on every page or from the dashboard). The chat window opens with a friendly greeting: “Hi, I’m your ACT Tutor Bot! How can I help you today?”
2. **Student’s Question:** The student types: “I got a math question wrong about functions. It said f(x) = 2x^2 – 3x + 1, and asked for f(3). I answered 7 but it was wrong. Can you explain it?”
3. **AI Context Processing:** The AI recognizes this as a math problem. It sees the function and the student’s attempt. It might reformulate: “Sure. You have f(x) = 2x^2 – 3x + 1 and you need f(3). Let’s solve that step by step.”
4. **AI Response:** The AI tutor breaks it down: “To find f(3), substitute x = 3 into the function. First, calculate 2\*(3^2). 3^2 = 9, and 2*9 = 18. Next, calculate –3*3 = –9. Now add the constant 1. So f(3) = 18 + (–9) + 1. 18 – 9 = 9, and 9 + 1 = 10. So f(3) = 10. The correct answer was 10, not 7. It looks like you may have made a calculation error; perhaps you forgot the +1 at the end?”

   - The answer includes the step-by-step calculation and identifies the likely mistake.

5. **Student Follow-up:** The student sees the explanation and realizes they mis-added. They reply: “Oh, I see. I think I added wrong. Thanks. Can we try another one like that?”
6. **AI Adaptive Response:** The AI says, “Sure! Let’s practice another function question.” It either pulls a similar question from the question bank or generates one: “Try this: g(x) = x^2 – 4x + 2. What is g(4)? You give it a try, and I’ll check your answer.”
7. **Student Solves with AI:** The student calculates and says: “I think it’s (4^2 – 16 + 2) = (16 – 16 + 2) = 2.”
8. **AI Feedback:** The AI replies: “Great work! Let’s check: 4^2 = 16, –4\*4 = –16, add 2 gives 16 – 16 + 2 = 2. Correct! Well done – you nailed it.”

   - The AI provided positive feedback and confirmed the solution.

9. **Student Asks Conceptual Question:** Now the student asks, “Why do we plug in 3 for x? I was a bit confused about function notation.”
10. **AI Explanation:** The AI explains the concept: “In function notation f(x), the x is a placeholder for the input. f(3) means we are inputting 3 wherever x appears in the formula. It’s like a machine: put 3 in, and the function produces an output. Does that make sense?”
    The student responds yes.
11. **Closing and Recommendation:** The AI might conclude, “Glad I could help! Would you like some tips on function questions or to try more practice? Or we can move to another topic if you want.”
    If the student is done, they close the chat. If not, they could continue in this conversational manner on other issues.

In this session, the AI tutor did a few key things: explained a missed question, provided an additional practice problem with evaluation, clarified a conceptual doubt, and offered further help.

#### UI/UX Considerations

- **Chat Interface:** Should be easily accessible (perhaps a chat icon floating on relevant pages or a dedicated “Tutor” page). The chat window could overlay on the current screen or be a separate full-page chat area.

  - The interface should show the conversation history with alternating user and AI messages, in speech bubble style or similar.
  - Allow basic text formatting by the AI for clarity (bullet points, maybe LaTeX or image support for math formulas/diagrams).
  - Provide quick action buttons for certain suggestions. For example, if the AI says “Shall we practice more?”, it could present buttons like “Yes, give me a question” or “No, thanks” for convenience.

- **Voice Integration (Future):** Possibly allow voice input/output – a student could speak a question and hear the AI’s answer. This is not required, but something to consider for accessibility and ease (especially on mobile).
- **Indicator of Thinking:** When the student asks a question, the AI might need a second or two to formulate an answer. Use a “typing…” indicator or spinner so the student knows the system is working.
- **Educational Tone:** The chat UI might include the tutor’s “avatar” – e.g., an icon of a friendly teacher or a robot – to give it a persona. The tone of responses should be supportive and never condescending. If the student is wrong, the AI should say things like “Not quite, here’s where it went wrong…” rather than just “Wrong.”
- **Integration with Content:** If the AI references a lesson or wants the student to do a specific quiz, it could send a link in the chat that the student can click to open that resource. (E.g., “I recommend reviewing \[Link: Comma Usage Lesson] and then trying \[Link: Punctuation Quiz].”)
- **Session Memory:** The AI should remember at least the current conversation context so the student doesn’t have to repeat themselves. Ideally, it should also recall prior sessions to some extent (“As we discussed yesterday, ...”) but that can be complex. At minimum, within one chat session, it has memory of what was said.
- **Exit and Save:** If the student closes the chat, perhaps save the conversation so they can refer back to it later (at least recent history). Or allow them to copy important solutions from the chat.
- **Limits and Expectations:** Maybe have guidance for students visible, like examples of questions to ask (“Try asking me: ‘Explain why my answer in question 3 is wrong’ or ‘Give me a formula for ...’”). This can guide them to get the most out of the tutor.
- **Error Handling:** The AI might sometimes not understand or might falter. If it cannot provide a good answer, it should at least respond with something helpful like, “I’m sorry, I’m not sure about that. Let’s try rephrasing or ask a different way,” rather than giving a useless or wrong answer.
- If the AI ever provides an incorrect answer or the student suspects so, there should be an easy way for the student to flag it (“Was this answer helpful? 👍/👎”). Negative feedback can be logged for admin review to improve the AI’s training or rules.
- **Loading Knowledge:** The AI might have access to the structured data (like the question bank with solutions, the lesson texts, etc.). It should ideally use those to ground its answers. That’s an implementation detail, but from UI perspective, the answers could sometimes quote from a lesson or use images from content for better explanation.
- **Privacy in Chat:** Since students might reveal personal academic struggles, ensure the chat data is stored securely. Possibly clarify that chat data will be used to help them and improve the AI, but kept private.

#### Performance Requirements

- **Latency:** Aim for responses in under \~3 seconds for typical queries. Long delays will frustrate users. Achieving this may require using efficient AI models or caching common Q\&A. If the AI is using an external API, ensure adequate throughput and handle delays gracefully (with a message like “This is a tough one, let me think…”, if it’s going to take a bit).
- **Scalability:** If many students chat with the AI simultaneously (e.g., the night before the ACT, hundreds might be asking questions), the system should scale. Use of a scalable AI service or multiple instances of the model might be needed. Implement rate limiting per user as needed (for cost control too).
- Possibly queue long requests so the system doesn’t overload. But try to maintain interactivity.
- **Session Management:** The AI service should handle multiple parallel sessions. Ensure user A’s context doesn’t bleed into user B’s answers (strict isolation of conversations).
- **Resource Use:** AI calls can be expensive; the system might limit the length of conversation context it sends to manage costs. But that’s back-end; from product perspective, perhaps limit one question at a time or discourage extremely long queries.
- **Fallbacks:** If the AI service fails (e.g., network down or API limit reached), the system should not crash. Show an error in chat: “Sorry, I’m having trouble reaching my knowledge base right now. Please try again later.” Also log this event.
- Possibly have a minimal rule-based backup for simple FAQs if the AI is down (like if student asks “How do I reset password?” which is not really a tutor question but could come, the AI or system can respond even if main AI is offline).

#### Security and Privacy Considerations

- **Data Privacy:** Conversations with the AI might contain personal data (a student might say “I have ADHD, I struggle with focus” or similar). Treat chat logs as personal data. Limit who can view them (perhaps only the student and system internally). If logs are stored for improvement, ensure they are anonymized if used by developers.
- **Compliance:** If using a third-party AI API, ensure it doesn’t improperly store or use student data. We may need a Data Processing Agreement with the provider (especially under GDPR, sending user data to an AI service counts as processing). Possibly allow opt-out of AI data sharing in privacy settings for extra-cautious users (with a warning that then AI tutor may not function).
- **Content Filtering:** Put guardrails on the AI:

  - If a student asks something abusive or unrelated (e.g., “Tell me a joke” – harmless but off-task, the AI can respond briefly and steer back to ACT; or “How do I cheat on the ACT?” – the AI should refuse that).
  - Ensure the AI won’t produce any harassing, inappropriate content. Use moderation filters to catch profanity or sensitive topics. For example, if a student types something distressing (“I’m so stressed I want to quit”), the AI should respond supportively and possibly suggest positive coping strategies or encourage seeking help, _not_ something harmful.

- **Accuracy/Safety Net:** We might include a disclaimer in the UI: “Our AI Tutor is here to help, but it’s not perfect. If something looks wrong, double-check with official sources or ask an instructor.” This sets expectations that it’s a guide, not absolute truth, though we aim for high accuracy.
- **Admin Monitoring:** For quality control, admin or content team might review anonymized transcripts. If so, mention it in privacy policy. This can help catch any consistent errors in AI responses and improve the system.
- **User Controls:** If a student doesn’t want to use the AI, they can ignore it. Possibly allow them to hide the chat interface if they prefer not to see it.
- **Model Updates:** If the AI is updated (improved model or knowledge), ensure regression testing that it still behaves helpfully. Possibly version the AI responses so if any issues, can roll back.
- **No Leaking Answers:** Make sure the AI does not just give away answers to tests the student hasn’t taken yet. For example, if asked “What’s the answer to question 10 in Practice Test 2?”, the AI should ideally refuse or encourage solving it rather than just providing it (this might be managed by not feeding the AI the answer keys in a way that it would answer such a query straightforwardly).

Overall, the AI Tutor should simulate as much as possible a personal tutor who is always available, patient, and knowledgeable, thereby enhancing the one-size-fits-all nature of typical prep with a customized learning experience.

## Admin Dashboard

The Admin Dashboard is a secure, back-end module for administrators (and possibly educators with permissions) to manage the platform’s content, users, and settings. It provides internal controls to keep the system updated and running smoothly. This section outlines features for product administrators (company staff who maintain the product). In cases where the platform is used by a school or tutoring center, certain admin functions might be delegated to their staff (like a teacher managing their class), likely via role-based access controls.

### Key Features and Functional Requirements

- **Admin User Management:**

  - **User List and Search:** View all student accounts (and any other roles). Ability to search by name, email, or ID. Results show key info (name, email, sign-up date, last login, subscription status).
  - **User Profile Actions:** Select a user to view detailed info: profile data, progress (scores), subscription plan, etc. Admin can perform actions: reset password for the user (trigger password reset email), edit their profile details if needed (e.g., correct an email typo), or deactivate/ban the account (prevent login) if necessary.
  - **Role Management:** Create or assign roles. For instance, mark a user as an “Instructor” which gives limited admin privileges (like viewing certain analytics). Or promote someone to an “Admin”. The system should support roles like Super Admin (full access), Content Manager (manage lessons but not payments maybe), Teacher (manage a set of students). Role-based access ensures each admin sees the appropriate sections.
  - **Bulk Actions:** Perhaps import users (for adding a class roster at once) or export user list (to CSV for record-keeping).

- **Content Management:** A critical piece for keeping the content fresh and correct.

  - **Question Bank Management:** Interface to add, edit, or remove questions in the database.

    - Add a new ACT question: include the question text, answer choices, correct answer, explanation, difficulty level, topic tagging (e.g., “Algebra>Quadratic Equations”), and which test form it belongs to (if it’s part of a specific practice test).
    - Edit existing question: fix typos or change an explanation.
    - Possibly import questions in bulk via spreadsheet for efficiency.
    - Ensure that changes to questions propagate to tests/quizzes using them.

  - **Test Forms Management:** Create or edit practice tests by assembling questions.

    - For example, define “Practice Test 3” by selecting 75 English Qs, 60 Math Qs, etc., from the bank. Set their order. Save the test form.
    - Or generate a test form from a pool randomly (though likely manually curated to match difficulty distribution).
    - Ability to retire or archive old test forms (so new students don’t use them, but maybe they remain for those who did).

  - **Lesson Content Management:**

    - Upload videos: probably by providing a video file or link, with a title, description, associated topic, and duration metadata. The system might handle storage or use an external video host behind the scenes.
    - Create/edit text lessons: a rich text editor to input formatted text, images, links. E.g., an admin can paste in the content of a “Tips for Reading” article or update it.
    - Create/edit quizzes: similar to question bank, but specifically smaller sets. Possibly reuse questions from the bank or write unique ones for the quiz. (Likely reuse for consistency).
    - Organize topics: Admins should be able to create new topics or rearrange content structure (like add a new subtopic under Math if needed).
    - **Publishing**: The CMS might have a draft/publish system. E.g., prepare content unseen by users, then publish when ready. Not mandatory but useful for previewing.

  - **Content Metadata:** Tag content with difficulty or ACT score level, so that recommendations can use that (if an advanced feature).

- **Analytics & Reporting for Admin:** (Though detailed separately in Analytics section, the admin dashboard will surface key analytics.)

  - **Platform Overview:** Show metrics like total users, active users (last 7 days), number of tests taken, average improvement, etc. Could be charts on an admin home page.
  - **Student Performance Analytics:** Possibly allow an admin to pick any student and see a performance report (similar to what the student sees, but accessible by admin, useful for support calls – e.g., a parent says their kid’s scores aren’t improving, admin can quickly check their history).
  - **Cohort Analytics:** If grouping is supported (classes, etc.), admin/teachers can view that group’s analytics (average scores, hardest questions, etc., see Analytics section).
  - **Content Usage Analytics:** Stats like “Most watched videos”, “Least attempted quizzes” to help content team identify what’s popular or what might need improvements. Also track AI tutor usage stats (# of questions asked, common queries).

- **Notification Management:**

  - **Template Editing:** Admin can edit the templates of emails/SMS that go out (e.g., reminder email text, welcome email text). Possibly through a simple editor with placeholders (e.g., “Hello {{name}}, don’t forget ...”).
  - **Schedule/Trigger Config:** Configure rules for notifications – e.g., set the system to send a “inactive for 7 days” email. If a certain date (like upcoming official ACT date) is near, maybe schedule a message to all users who have that date set.
  - **Announcement Broadcast:** A tool to send a custom email or in-app announcement to all users or a segment. For instance, “We added new lessons in Math – check them out!”.
  - **View Notification Logs:** See a log of major communications sent (for auditing that important emails went out).

- **Payment and Subscription Admin:**

  - **Subscription Overview:** List of all active subscriptions, their plan types, next billing dates, etc. Possibly integration with the payment provider to show status.
  - **Manage Individual Subscription:** For example, if a customer support request comes in to refund or cancel, the admin can do so through the dashboard:

    - Cancel a subscription (which sets it to not renew).
    - Issue a refund (if integrated or at least record it and then process via payment gateway dashboard).
    - Change a user’s plan (upgrade/downgrade manually).

  - **Promo Codes Management:** Create and manage promo codes (discounts) if marketing runs promotions.
  - **Billing History:** Access user’s billing history/invoices if needed to resend a receipt.
  - (Some of this may be done directly in Stripe’s dashboard if using Stripe, but replicating key functions in our admin can streamline support.)

- **System Configuration:** Miscellaneous settings:

  - ACT test date calendar – update upcoming official ACT dates in the system (if we use those for reminders).
  - Feature toggles – e.g., turn on/off the AI tutor module (if needed for maintenance).
  - Content version – maybe push updates or flush caches.
  - Manage supported locales (if future multi-language).

- **Audit Logs:** For security, log admin actions (especially destructive ones like deleting a user or modifying content) so we have a history of who did what. Possibly present these logs in admin UI if needed.
- **Role-based Access & Security:** Ensure that within the admin dashboard, an admin sees only what they should:

  - A full admin sees everything.
  - A content manager might see only Content Management and basic analytics, but not financial info.
  - A teacher might see only their students and related analytics, not the entire user base or platform settings.
  - Use a consistent navigation but with sections hidden or disabled based on permissions.

- **Ease of Use:** The admin interface should prioritize clarity and efficiency since staff will use it regularly to perform tasks. It might be more utilitarian in design compared to student-facing parts, but still user-friendly to reduce training needs.

#### User Stories (Admin Dashboard)

- _As an admin,_ I want to **search for a student account** and view their details so that I can assist with support requests (like checking their progress or troubleshooting issues).
- _As an admin/content manager,_ I want to **add and update practice questions and solutions** in the system so that content stays accurate and we can introduce new material for students.
- _As an admin/content manager,_ I want to **upload a new video lesson and create a quiz** for it so that students have up-to-date learning resources for a new ACT topic or strategy.
- _As an admin,_ I want to **disable a user account** if I detect abuse or if requested (e.g., account deletion) to maintain the community and privacy standards.
- _As an admin,_ I want to **broadcast an announcement** to all users (or a subset) about an upcoming feature or a scheduled downtime so that users are informed.
- _As a customer support admin,_ I want to **manage a user’s subscription** (cancel, refund, change plan) in response to a customer inquiry, to ensure billing issues are resolved quickly.
- _As an admin,_ I want to view **overall usage statistics** (like how many tests taken this month, average score improvements, active users) so I can report on the platform’s performance and engagement.
- _As a teacher (institutional user),_ I want a limited admin view where I can **enroll my students**, assign them content or tests, and then later **view their scores and progress**, but not see other instructors’ students or system-wide settings.
- _As an admin/security officer,_ I want to see an **audit log of admin actions** to track changes for compliance and be able to investigate if something was changed incorrectly.

#### Example Use Case: Updating Content and Monitoring Usage

1. **Logging In:** An administrator navigates to an admin-specific URL (e.g., `admin.platformname.com`) and logs in with admin credentials (with 2FA if enabled for admins). They reach the Admin Dashboard home.
2. **Dashboard Overview:** The homepage shows some key stats: e.g., “5000 active users, 200 new sign-ups this month, 1200 practice tests taken this week”. It also shows any system alerts (like pending content approval or errors). It has a navigation menu for Users, Content, Analytics, etc.
3. **Content Update:** The admin chooses **Content > Questions**. They search for a question ID or text to find a specific math question that was reported as having a typo. They find the question, edit the text in a rich text field to fix the typo, and save. The system updates the question bank. Because that question appears in Practice Test 2, it’s now fixed for all future test-takers.
4. **Adding a Lesson:** Next, the admin goes to **Content > Lessons**. They click “Add Lesson”. They input:

   - Title: “New ACT Calculator Policy Changes 2025”.
   - Type: Article (text).
   - Subject: Math, Topic: “Calculator Use”.
   - Content: they paste an article explaining new policies (with formatting).
   - They hit Save Draft. They review how it looks in a preview. Then Publish.
   - Now that lesson is live; they might also want to notify users, so they schedule an announcement or let marketing know.

5. **User Management:** The admin gets a support ticket: a student can’t log in. They go to **Users** and search by the student’s email. They find the user. Perhaps the issue is the email was not verified. They see a “Resend verification email” button and click it. Or if the email was wrong, they correct it and then resend.
6. **Analytics Check:** End of the month, the admin needs to report improvement stats. They go to **Analytics** section:

   - They select a date range (e.g., last 3 months) and view “Score Improvement Report”. The system shows that among users who’ve taken 2 or more full tests, the average composite score improvement is +3 points.
   - They also see a breakdown by usage: those who used the AI tutor frequently improved more, etc., which is interesting data.
   - The admin exports some charts or data as needed for a report (maybe as CSV or screenshot).

7. **Notification Broadcast:** The admin wants to remind all trial users to consider subscribing. They go to **Notifications > Email Broadcast**. They filter user list by “trial users” (users who signed up but haven’t paid and are within their trial period).

   - They compose an email using a template, maybe something like “Your free trial is ending, here’s why to upgrade...” and schedule it to send tomorrow morning.
   - The system will send that email out to those 100 users and provide a log.

8. **Role-specific scenario:** A teacher at a partner school has been given an instructor login (with limited rights via role).

   - The teacher logs in and can only see their class of, say, 30 students. They see a pared-down dashboard showing those students’ average scores, etc.
   - They can click a student to see that student’s latest test results and perhaps assign content (maybe assigning content is a feature: e.g., mark certain lessons as “homework” for their class).
   - The teacher cannot access global user lists or billing—only their domain.
   - (This scenario is optional depending on whether B2B usage is planned, but it demonstrates the need for role segmentation).

9. **Security Auditing:** Suppose a content error was found – a question was accidentally deleted. The lead admin checks **Audit Logs**. They find that an admin account “JaneDoe” deleted Question ID 1234 two days ago. They realize Jane did so unintentionally. They can then re-add the question or at least understand what happened. This log helps avoid confusion or misuse.
10. **Maintenance:** Admin might also use the dashboard to put the site in maintenance mode (e.g., a toggle that shows a “Maintenance, back soon” banner to users, used when deploying a major update). This could be under a Settings section.

Throughout, the admin dashboard ensures that those running the platform can do so efficiently without database edits or developer intervention for routine tasks.

#### UI/UX Considerations

- **Layout:** Likely a sidebar or top menu for admin sections. Could use a standard admin template style (not too flashy, but clear).
- **Tables and Forms:** A lot of admin interactions involve tables (user lists, content lists) and forms (entry/edit forms). Use sorting, filtering, pagination for tables if records are numerous. Allow toggling columns on/off maybe.
- **Responsive**: Admins might access on various devices; ensure it’s usable on at least tablet size. Desktop usage is primary.
- **Confirmations:** For destructive actions (delete user, remove question, etc.), require confirmation (maybe type “DELETE” or at least click confirm) to prevent accidents.
- **Validation:** In forms, ensure required fields are marked, and validate data (e.g., don’t allow creating a question with no correct answer marked).
- **Rich Text/Media Management:** Content editing should be WYSIWYG for ease. If uploading images (for a lesson or question diagram), provide an upload interface and manage file storage.
- **Preview:** For content, an admin should preview how it will look for students. Possibly an “Impersonate user” feature can let admin see the student view (read-only) for debugging.
- **Performance for Admin:** Admin pages should also be fairly snappy, but can tolerate being a bit heavier than student pages. However, searching a user among 10k should be quick (index DB properly).
- **Security:** The admin dashboard must be extremely secure:

  - Only accessible by admin accounts.
  - Possibly IP-restricted if internal use (maybe not, since remote work).
  - Definitely enforce strong passwords and 2FA for admins to reduce risk of compromise, because an admin account has access to all data.
  - Use distinct subdomain and perhaps additional login steps for admin.

- **Logs:** If an admin action triggers notifications (like if an admin changes a user’s email, an email confirmation to the user might be auto-sent for security), the UI should inform the admin that happened.
- **Feedback:** Show success messages or errors clearly on admin actions. For example, “User data updated successfully” or “Error: email already in use by another account” etc.
- **Help for Admins:** Perhaps a help section for admins too, or tooltips in the admin UI explaining fields (especially for complex tasks like “score conversion table upload” if that exists).
- **Audit UI:** If providing an interface to view logs, make it searchable by date/admin user, etc., so one can trace what happened on a given date.

Admin Dashboard is essentially the control panel of the platform – designing it well ensures efficient operations and content upkeep, which directly affect the quality of the student experience.

## Analytics and Reporting

Analytics and Reporting provide insights into student performance and platform usage. This module includes **student-facing analytics** (so learners can understand and track their own progress) as well as **cohort or system-level analytics** for admins or instructors to gauge effectiveness and identify trends. The analytics should turn raw data (test scores, question responses, study time) into meaningful information and visualizations.

### Key Features and Functional Requirements

- **Student Performance Dashboard:** For each student (accessible to the student themselves and authorized viewers like their teacher or admin):

  - **Score Trends:** Graphs showing the student’s score progress over time for each ACT section and composite. For example, a line chart where X-axis is test date and Y-axis is score, with separate lines for English, Math, Reading, Science, and maybe composite. This lets them see improvement or any plateaus.
  - **Section Breakdown:** A snapshot of current proficiency in each section. E.g., “English: 25 (target 30), Math: 28 (target 30), …” possibly with a visual like a bar showing how close to target or to the max 36.
  - **Subscore/Topic Analysis:** If the system tags questions by content area, provide a breakdown by topic. For example:

    - In Math: “Algebra: 80% correct (strong), Geometry: 50% correct (needs improvement), Trigonometry: 60%.”
    - In English: categories like Usage/Mechanics vs Rhetorical Skills percentages.
    - Reading: performance by passage type maybe (Prose vs Science passage).
    - Science: performance by data interpretation vs experiment analysis, etc.
      This can be shown with bar charts or a table of strengths/weaknesses.

  - **Time Analysis:** Stats on time management if available: e.g., average time per question in each section vs the time allowed. Did the student consistently run out of time in Reading? If data exists (we can gather how many questions left blank or guessed at end due to time).
  - **Practice Activity:** Number of practice tests taken, number of quizzes completed, total questions answered on the platform. Possibly a “study hours” metric if we track time spent on videos and tests.
  - **AI Tutor Usage Impact:** If possible, correlate use of AI tutor with performance: e.g., “You asked 10 questions to the AI tutor this week. Your quiz scores improved by 5% in topics discussed.” (This is advanced and might not be in initial version, but as a concept).
  - **Achievements/Milestones:** Show any notable achievements, like “Improved Math by +4 points since starting” or “Completed all Reading lessons.”

- **Cohort Analytics (for Teachers/Admins):** If grouping of students is supported (class, tutoring group, or even all users as a whole for internal analysis):

  - **Group Overview:** For a selected group of students (or all students):

    - Average score in each section, distribution of scores (perhaps a box plot or just min/median/max).
    - Number of students who have reached certain benchmarks (e.g., how many are 30+ in Math, etc., useful for teachers aiming for goals).
    - Progress distribution: e.g., “10 out of 30 students improved since last test, 5 stayed same, 15 haven’t taken a new test.”

  - **Comparative Analytics:** Compare one cohort to another (maybe compare two classes if a school admin, or compare a student to the cohort average).

    - E.g., Student A’s score vs class average on each section.
    - Or one class’s average composite vs another class (for internal competitions or evaluations).

  - **Question Analysis:** Identify questions or topics most missed by the cohort:

    - “In the last test, Question 32 (Science) only 20% of the class got it right – might indicate that topic is not well understood.”
    - This can help instructors pinpoint topics to review in class.

  - **Engagement Metrics:** For a teacher or admin: see which students are not utilizing the platform enough (e.g., “5 students haven’t taken any practice test in 3 weeks”) so they can intervene.

- **Platform-wide Analytics (Admin):**

  - User growth over time (sign-ups per week).
  - Engagement over time (active users per day).
  - Average improvement of all users who’ve taken at least 2 tests.
  - Perhaps efficacy metrics like correlation between content completion and score gain, etc. (This is more internal, but valuable to product team to prove the platform’s value).
  - Could integrate with business metrics (though more for internal product team than needed in PRD).

- **Reporting Features:**

  - Ability for users (students or instructors) to export a report of performance. For example, generate a PDF report card that summarizes the student’s performance (could be used for parent meetings or personal tracking).
  - Scheduled reports: e.g., email a weekly progress summary to the student or parent. (This crosses into notifications).
  - Custom reports: an admin might select some data range or filter (like all students who started in a certain program) and export data for research.

- **Data Freshness:** Analytics should update promptly after new data is available:

  - After a student completes a test, their personal analytics updates immediately with that new score.
  - Cohort analytics might update in real-time or near real-time (or perhaps daily aggregated for heavy stuff).
  - Use a background process for heavy aggregation if needed, but ensure it doesn’t lag too much.

- **Adaptive Insights:** Provide insights or tips based on analytics:

  - For example, if a student’s Reading score has plateaued for 3 tests, show a note: “Your Reading score hasn’t improved recently. Consider focusing on time management in that section.”
  - Or cohort insight: “Class 101 improved average Math by 2 points after completing the Algebra lesson series.”
  - These can be shown on dashboards as little callouts.

- **Benchmarking:** Possibly allow students to compare their performance to broader benchmarks:

  - Compare to the average of all platform users, or to national ACT averages (if data known: e.g., “Your 24 is above the national average of \~21”).
  - But careful with privacy and morale—this is optional.

- **Goal Tracking:** If a student set a target ACT score, analytics can show progress toward that goal (like a progress bar or “6 points to go!”).
- **Data Visualization:** Emphasize easy to understand visuals: line charts, bar charts, pie or radar charts for topic breakdown, etc., with labels and maybe interactive tooltips for details.

#### User Stories (Analytics & Reporting)

- _As a student,_ I want to see **graphs of my practice test scores over time** so that I know if I’m improving and by how much.
- _As a student,_ I want to identify my **strong and weak areas** on the ACT, so the analytics should show my performance by topic (e.g., I’m good at Algebra but weak in Geometry) so I know where to focus.
- _As a student,_ I want to track **how much I’ve practiced** (hours, number of questions) and how it correlates with my score improvement, so I can gauge if I’m doing enough.
- _As a student,_ I want to **celebrate milestones** (like first time scoring above 30 in a section) via the dashboard because it motivates me to continue.
- _As a teacher,_ I want to view a **report of my class’s performance**, seeing each student’s latest score and improvement, so I can intervene with those who are lagging and praise those doing well.
- _As a teacher,_ I want to see which **topics my class as a whole struggles with**, so I can revisit those topics in instruction (e.g., if most of my class misses punctuation questions, I’ll do a punctuation workshop).
- _As a teacher,_ I want to easily **export or print reports** for each student to share with their parents during meetings, to discuss their progress with data.
- _As an admin,_ I want to analyze **overall user engagement and performance trends** (e.g., do users who use the AI tutor improve faster? Do those who complete all lessons reach target scores?) to inform product decisions and prove the effectiveness of the platform.
- _As an admin,_ I want to monitor if **cohorts using our platform perform better on the real ACT** (if data available or through user self-report of actual ACT scores later) to assess outcomes.
- _As a student,_ I want to possibly **compare my scores to others** (anonymously/averages) to understand where I stand (though this can be sensitive, it can be optional benchmarking).
- _As a parent (if they have access to reports),_ I want to receive a **weekly email summary of my child’s practice and improvements** so I can stay informed and support their study plan.

#### Example Use Case: Student Checking Progress and Teacher Monitoring Class

**Student’s Perspective:**

1. After logging in, the student goes to the “Progress” tab on their dashboard.
2. They see a **score trend chart**. For example, four points on the chart for Composite score: 22 → 24 → 23 → 26 over the last two months. Hovering on each point shows the date and test name. They notice a dip on the third test and then a jump on the fourth.
3. They scroll and see **Section performance**: a bar graph or set of gauges. E.g., English 25, Math 28, Reading 24, Science 27 (all out of 36). If their goal is 30 each, maybe the bars show current vs goal. Reading is the lowest, maybe highlighted or an icon suggesting “Needs attention”.
4. Next, **topic breakdown**. Perhaps a table:

   - English: Grammar 85% correct (strong), Punctuation 70%, Rhetorical 65%.
   - Math: Algebra 90%, Geometry 50%, Trig 40% (weak – trig likely a small portion but clearly an issue).
   - etc.
     These might be color-coded (green >80%, yellow 50-79%, red <50%). The student can identify Geometry and Trig as weak spots in Math.

5. The student also sees **analytics insights**: a small note: “Your Math score is strong overall, but Geometry/Trig are dragging it down. Consider reviewing those topics. Your Reading score improved significantly after focusing on time management – keep it up!”
6. There is also a section showing **time spent**: e.g., “You have taken 4 full tests and 10 quizzes, totaling \~8 hours of practice. On average, our high scorers practice \~15 hours. Keep going!”
7. The student can click to generate a **Progress Report PDF**. This compiles their charts and stats into a nicely formatted document (with perhaps the platform logo and their name, good for sharing with a tutor or parent).
8. Feeling motivated, the student knows exactly what to work on next (Geometry and Trig). They head to content or ask the AI tutor for help in those areas.

**Teacher’s Perspective (Class Cohort Analytics):**

1. A teacher logs into their instructor account and accesses the **Class Analytics** for “Period 5 ACT Prep”.
2. They see a roster with each student’s latest composite and the change since last test in parentheses. For example:

   - Alice: 25 ( +2 )
   - Bob: 18 ( -1 )
   - Charlie: 22 ( 0 )
   - ... etc.
     So they immediately spot Bob dropped by 1 and is at 18, needs attention, whereas Alice improved nicely.

3. They click a “View details” for Bob. It shows Bob’s trend and that he’s weak in Science. The teacher now knows to maybe give Bob extra Science practice.
4. The teacher also sees an aggregate chart: e.g., class average composite started at 20 and is now 23. Good improvement as a whole.
5. **Topic difficulty analysis:** The teacher sees something like “Class Accuracy by Topic: Algebra 75%, Geometry 40%, Data Representation (Science) 50%, etc.” If Geometry is low across many students, the teacher deduces to review Geometry in class.
6. The teacher downloads a **Class Report** PDF that shows how many students are in each score band (like a histogram of scores). They might share this with the school administrator or use it to tailor their curriculum.
7. The teacher also uses the system to send each student’s report to their parents (if emails are connected). Possibly via a built-in feature: “Email progress reports to parents” which pulls the PDF for each student and emails it.
8. The teacher’s admin view respects privacy—students only see their own, teacher sees only their class, not others.

**Admin’s Perspective (Platform-wide):**

1. The product manager/admin looks at a **global analytics dashboard** (maybe separate from the teacher interface):

   - e.g., “Average initial score: 19, Average latest score after 1 month: 23, average improvement +4”.
   - They might see usage: “70% of users who sign up take at least one test. 30% use the AI tutor. Among those who used AI tutor, improvement is on average 1 point higher.” (Hypothetical insight gleaned).
   - This helps them identify the AI tutor’s value or if it’s underutilized.

2. They also see which content is most viewed. Suppose “Math Basics video” has 500 views, but “Trigonometry video” only 50. Maybe because fewer get to that advanced content, or maybe it’s hidden – they can investigate why.
3. If integrated, they could see data from any official scores students enter after taking the real ACT to gauge real outcomes. (This requires students self-report or linking to official data, which may not be in initial scope).
4. Admin uses these insights for marketing (“our students improve 4 points on average!”) and for product decisions (“we need more geometry content” or “why are users not doing many quizzes – maybe make them more prominent”).

#### UI/UX Considerations

- **Visual Clarity:** Use intuitive charts:

  - Line charts for trends (with clear axes labels and maybe goal lines).
  - Bar charts or radar charts for topic proficiency (radar could show a profile across subjects).
  - Pie or Donut charts for breakdown like time allocation (less critical).
  - Tables for detailed breakdowns with conditional formatting (color highlights).

- **Interactivity:** If feasible, allow users to toggle which test results to include in trend (like include/exclude a diagnostic if it was an outlier), or hover to see exact values.
- **Responsive:** Ensure charts are viewable on mobile – perhaps use slightly different layouts (stacked vertically).
- **Downloadable Reports:** Provide export to PDF or image for charts. Ensure the PDF layout is polished (maybe a cover page, nice formatting).
- **Comparisons:** If showing comparisons (like student vs average), ensure privacy (only show class average to that class’s instructor, not individual peer comparison to student unless anonymity).
- **Filters:** On class analytics, allow filtering by date range or by type of test (maybe differentiate official practice tests vs quizzes).
- **Explanations:** Provide context or explanations with analytics:

  - For example, next to a chart, a sentence summarizing: “You improved by 4 points overall – great progress!”
  - Or “Geometry is your weakest topic (50% correct). We recommend reviewing those lessons.”

- **Clean UI:** Possibly dedicate a full page to analytics with sections or tabs for different data. Avoid clutter. Use accordions or tabs if needed (e.g., a tab for “By Topic” vs “By Time”).
- **Data Accuracy and Trust:** If any analytics might be confusing, add an info icon. E.g., “How is composite calculated here? We use the same method as ACT: an average of section scores.”
- **Live vs Historical:** Make it clear what data is current vs old. E.g., label the latest test clearly, or if student hasn’t taken a test in 60 days, maybe a nudge “It’s been a while since your last practice test.”
- **Privacy:** If a teacher views class analytics, they should not see any other class data. And probably they shouldn’t see student names of another class. Multi-tenant separation must be solid for schools.
- **Real vs Practice:** If at any point we incorporate real ACT scores (maybe a student enters their official score after taking the exam to see how it compared to practice), ensure we differentiate official vs practice in the analytics.
- **Loading and Performance:** Generating analytics might involve lots of data. Use loading spinners or async loading for heavy components. Possibly precompute a lot of it nightly for quick load.
- **Accuracy**: Ensure calculations (like percent correct, score improvements) are correct and up to date. Validate using test scenarios to avoid off-by-one or mis-averaging that could mislead.
- **Gamification and Motivation:** Perhaps incorporate small “rewards” in analytics: e.g., badges or messages like “Consistency Badge: you practiced 5 days in a row!” on the analytics page. This ties into engagement more than pure analytics but can be placed there.

Analytics and reporting ultimately should empower students to self-reflect, motivate further improvement, and give educators the data to provide targeted support. It transforms raw performance data into actionable insights.

## Notification System

The Notification System covers all automated and manual messages sent to users outside the immediate web interface. This includes emails, SMS messages, and push notifications that keep users informed and engaged with the platform. Notifications are triggered by various events (e.g., completing a test, upcoming deadlines) or schedules (e.g., daily practice reminder) and are an important component for driving user engagement and providing a supportive experience.

### Key Features and Functional Requirements

- **Email Notifications:** Utilize email for longer or less time-sensitive communications:

  - **Account-Related:** Verification email on sign-up; welcome email with overview of resources; password reset emails; payment receipt emails for subscriptions; subscription renewal reminders; trial expiration warnings; account deactivation confirmations.
  - **Progress Updates:** Send the student a summary after each full practice test (e.g., “Your Practice Test Results: Composite 26 – see details on your dashboard”). Possibly attach or link to their full report.
  - **Scheduled Reminders:** If a student sets an official test date, schedule emails leading up to it: e.g., “Your ACT is in 1 month – here’s a study tip…”; “1 week left – good luck, here are last-minute pointers”; “Congrats on finishing the ACT! Enter your score to track results.”
  - **Weekly Digest:** Optionally, a weekly email summarizing their activity: “This week you completed 2 quizzes and improved your Math average by 3%. Keep it up!”
  - **Re-engagement:** If a user has been inactive for a certain period (no login or practice for, say, 10 days), send a gentle nudge: “We miss you! Your ACT prep awaits – how about a quick practice session today?”
  - **Announcements/Newsletters:** Inform users of new features or content (“New video lessons added in Science section!”) or general tips (“Tip of the week: Answer every question, no guessing penalty on ACT”).

- **SMS Notifications:** Use SMS for short, urgent, or high-attention messages (and only for users who opt in their mobile number):

  - **Reminders:** “Reminder: ACT Practice Test tomorrow at 10am – be ready!” or “Don’t forget to complete a practice quiz today to stay on track.”
  - **Short Progress Alerts:** “Congrats! Your latest practice test score: 25. Check your email for details.”
  - **Critical Account Alerts:** e.g., “Your subscription will renew tomorrow. Reply STOP to cancel or see email for details” (and ensure compliance with SMS opt-out rules).
  - SMS should be concise (160 chars or so). Use URL shorteners for any links.
  - Only send at reasonable times (maybe abide by quiet hours in user’s time zone).

- **Push Notifications (Mobile App):** If a mobile app is in use:

  - Real-time push for reminders (“Time to practice!” at scheduled times user sets or defaults).
  - Alerts like “Score report is ready” as soon as they finish a test (to draw them back in to review if they left the app).
  - “New content available” or “AI tutor has a tip for you today!” type pushes.
  - These should be configurable by user (some may only want certain types).

- **In-App Notifications:** A notification center within the web portal for non-intrusive alerts:

  - For example, a bell icon with notifications like “Your subscription is successfully renewed on May 1” or “Admin posted an announcement about upcoming features” or “You earned a Gold Badge for completing 5 tests”.
  - Less critical since email covers many, but in-app can consolidate and ensure user sees it next login without checking email.

- **Notification Preferences:** Allow users to control their notification settings:

  - In profile settings, checkboxes for “Email me weekly progress summaries”, “SMS reminders”, etc.
  - By default, essential ones (account, payment, critical alerts) are on and maybe cannot be turned off (except by unsubscribing entirely for marketing).
  - Marketing vs transactional: comply with laws (CAN-SPAM, etc.) by distinguishing the two. Provide unsubscribe link in promotional emails but still send transactional (like password reset) regardless.
  - Provide an easy way to opt out of SMS (e.g., reply STOP).

- **Scheduling and Throttling:** Implement logic to schedule notifications appropriately:

  - If a student finishes a test at 2am, maybe send the email immediately or next morning? Immediate is fine for email (they’ll see it when they wake), but for SMS maybe hold until morning.
  - Daily or weekly emails should be sent at an appropriate local time (if know time zone; if not, perhaps afternoon to catch after school).
  - Ensure not to spam: e.g., don’t send multiple inactivity nudges in the same week. And if they become active, cancel pending nudges.

- **Personalization:** Personalize content of messages:

  - Use their name, reference their goals (“You’re 4 points away from your goal score!”), and content related to their activity (“that geometry lesson you completed”).
  - For upcoming test reminders, mention the actual date and maybe location if they input (less likely we have location, but date for sure).

- **System Alerts:** If the platform will be down for maintenance, send an email or in-app alert ahead of time to inform users.
- **Admin/Instructor triggered messages:**

  - A teacher might want to send a message to all their students (“Reminder: complete Practice Test 2 by Friday”). The system should facilitate that via the admin dashboard (as discussed).
  - Admin announcements as well (which could route through email or just in-app).

- **Logging and Tracking:**

  - Keep logs of what notifications were sent to whom and when (for support and compliance).
  - If using email open/click tracking (for engagement analytics), ensure privacy policy covers that. But might help to know if users engage with reminder emails or not.
  - For SMS, track delivery status (if available from provider) and handle bounces (invalid numbers).

- **Compliance:**

  - FERPA: likely fine as these are communications about the student’s own data to themselves or authorized parties.
  - GDPR: need user consent for certain communications (especially promotional). During registration, ask for consent for marketing emails.
  - Provide clear unsubscribe in non-transactional emails.
  - For minors, possibly ensure content of notifications is appropriate and doesn’t reveal sensitive info (though all is academic).
  - SMS and email compliance like opt-out and including the identity of sender (the platform name).

- **Third-Party Integration:** Use reliable services to send:

  - Email: integrate with a service like SendGrid, Mailgun, AWS SES for deliverability.
  - SMS: integrate with Twilio or similar.
  - Push: via Firebase Cloud Messaging (FCM) for Android, APNs for iOS.
  - The system triggers events to these services through an automated scheduler or event-driven system (like after test completion event, trigger email).

- **Opt-in collection:** On user profile, allow adding a phone number for SMS with proper verification perhaps (send code to confirm number ownership) and a clear opt-in checkbox for SMS.
- **Multi-language support:** If platform is ever localized, notification templates need localization too, but initially likely just English (since ACT is English-based).
- **Scalability:** Able to send potentially large volumes (if 1000s of users get a reminder same day). Use batch sends for efficiency if possible. But the services mentioned handle scale by design.

#### User Stories (Notification System)

- _As a student,_ I want to receive a **reminder notification** the day before I planned to take a practice test so that I don’t forget to actually do it.
- _As a student,_ I want to get a **confirmation email with my score report** after I complete a practice test, so I have a record and can review it later.
- _As a student,_ I want to be **nudged if I become inactive**, for example via an email after a week of no study, because I might procrastinate and that reminder can push me to get back on track.
- _As a student with a busy schedule,_ I appreciate receiving **weekly summary emails** that highlight my progress and suggest next steps, so I can keep the big picture in mind even if I forget to log in daily.
- _As a student,_ I only want relevant messages – I should be able to **opt out of promotional emails** if I feel they’re too much, while still receiving important account or progress messages.
- _As an instructor,_ I want to **send a bulk message to my class** through the platform (rather than collecting emails manually) to remind them of an assignment or test, to save time and ensure everyone gets it.
- _As an admin,_ I want the system to automatically **welcome new users** with tips and orientation (via email) to increase initial engagement.
- _As an admin,_ I want to ensure **no user is spammed** – communications frequency should be controlled, and users should feel informed, not annoyed.
- _As a parent,_ if I sign up or if my child’s account lists my email for reports, I want to **get regular updates** on their progress (assuming the system supports parent CC on notifications).
- _As a user,_ I want notifications to be **timely and accurate** – e.g., a reminder should come at the right time, and a score report should show the correct data – so I trust the system and rely on it.

#### Example Use Case: Notification Journey

1. **Welcome Email:** A student signs up. Within minutes, they receive a verification email to confirm their address. After verifying, they get a **welcome email**: “Welcome to \[Platform]! Here’s how to get started: take a diagnostic test, explore our lessons, etc.” It’s personalized with their name and perhaps the date of their upcoming ACT if they entered one.
2. **Post-Activity Email:** The student takes a practice test. Upon completion (or maybe an hour later to allow them to review online first), the system sends an email: **Subject:** “Your ACT Practice Test Results – Great job!”. The body congratulates and summarizes: “Composite: 26, English:25, Math:27, Reading:24, Science:28. See detailed analysis on your dashboard.” It might highlight improvement: “That’s 2 points up from your last test!” and encourage sharing or next steps.
3. **Push Notification:** If the student has the mobile app, as soon as the test is graded, they also get a push: “You scored 26 on your practice test! Tap to review details.” Clicking it opens the app’s results screen.
4. **Weekly Summary:** On Monday, the student gets a weekly email: “Weekly Progress Update: You spent 3 hours last week, completed 1 test and 2 quizzes. Your strongest area is Math. This week, try focusing on Reading – here’s a recommended lesson \[link].” This keeps them engaged.
5. **Inactivity Nudge:** The student then gets busy and doesn’t log in for two weeks. The system triggers an inactivity email: **Subject:** “We’re here to help you get back on track”. Body: “Hi \[Name], preparing for the ACT is a marathon. It’s been 14 days since your last practice. How about doing a quick 10-question quiz today? Small steps add up! \[Button: Practice Now]”. Possibly also a push notification: “Haven’t practiced in a while? Jump back in with a quick quiz!”
6. **Subscription Reminder:** The student’s free trial is ending in 2 days. They get an email: “Your free trial ends soon – Upgrade to continue your progress!” with pricing info and a link to upgrade. Since it’s important, also maybe an in-app notification or push if not responded.
7. **Teacher Message:** Separately, in a classroom scenario, a teacher uses the admin interface to send a reminder: “Complete Practice Test 3 by Friday.” The system delivers this as an email to all students in that class (and maybe an in-app note). Each student gets: **Subject:** “\[Teacher Name] Reminder: Complete Practice Test 3 by Friday”. Body: message and maybe link to start that test.
8. **Official Test Approaching:** The student’s actual ACT date (from profile) is in 1 week. The system sends an encouraging email: “1 Week Until Your ACT – You got this! Last-minute tips: ... (list of quick tips).” Possibly also a SMS if opted in: “Your ACT is in 7 days. Stay calm, review your notes, and get good rest. Good luck!”
9. **Maintenance Notification:** The platform plans downtime for an update. All users get an email: “Platform Maintenance on Sat 5 PM – 6 PM CT. The site will be unavailable during this time.” and an in-app banner appears that day reminding them.
10. **Result Follow-up:** After the official test date passes, maybe an email: “How did it go? Enter your official score to see how you improved from your starting point.” (If we allow storing official scores for reflection.)
11. **Opt-out Example:** The student feels they don’t need weekly summaries. They go to settings and uncheck “Weekly summary emails.” The system then stops those for that user. They still receive important ones like password resets or trial end since those are transactional.

#### UI/UX Considerations

- **Email Design:** Use a clean, mobile-responsive email template with platform branding. Include the student’s name in the greeting for personalization. Key info should be near the top (people may not scroll long emails). Have clear CTA buttons (“Review Results”, “Continue Studying”) to drive them back to the platform.
- **Tone:** Keep tone friendly, motivational, and concise. For progress and reminder emails, positive reinforcement is key (“Keep up the good work”, “Don’t worry, you can improve with practice,” etc.).
- **Subject Lines:** Should be clear and appealing, not too marketing-like for critical ones. e.g., “Your ACT Progress Update” is straightforward; avoid spammy language or all caps.
- **SMS Format:** Identify the sender in SMS since short codes often don’t show a name: e.g., start with “\[PrepPlatform]: ...” in the message. Keep within 160 char to avoid split messages on some phones. Use very clear and brief content.
- **Opt-Out Info:** All bulk emails need an unsubscribe link (except purely transactional like password resets). Usually at the footer: “To unsubscribe from these updates, click here.” Similarly, SMS include “Txt STOP to unsubscribe” on the first message or all as required.
- **Notification Settings UI:** Under profile or settings, list categories with toggles. Possibly default all to on except SMS which requires adding number. Clearly label each (“Practice Reminders”, “Score Reports”, “Promotional Offers”, etc.). This gives user control and builds trust.
- **Push Notification Opt-in:** The app will ask permission for push. We should explain why: e.g., “Enable notifications to get reminders and updates on your progress.”
- **Frequency Capping:** If user performs many actions quickly (e.g., takes 3 quizzes in an hour), don’t email after each quiz – maybe consolidate or only send for major events (like full tests). Also, if multiple triggers coincide, combine into one email if possible (for example, trial ending and inactivity might overlap – one email can address both if timing aligns).
- **Testing and Quality:** We must test that all links in notifications go to the correct pages (e.g., deep link from push to specific screen, email links log in the user if needed or prompt to log in). Broken notification links would frustrate users.
- **International considerations:** If any user is international, ensure SMS country codes are handled and content is still relevant (though ACT is mostly US and territories).
- **Logging visible to user:** Possibly show in account settings a log of emails sent (some systems do this for transparency). Not necessary, but for instance, “Last email sent: Weekly Summary on Oct 10 to \[email].”
- **Error Handling:** If an email fails (bounces), mark that email as invalid and perhaps alert admin to follow up (especially if bounce on a verification email for a new user).
- **Double-check Sensitive Info:** Don’t include highly sensitive data in notifications in case someone else sees it. Scores are okay, but maybe don’t send their password in email, obviously. Also, maybe don’t include full account details or personal info in SMS since it’s less secure.
- **Rate Limits:** For SMS especially, ensure we don’t send too many in a short span to avoid carrier blocking or user annoyance. Likely just a handful per month at most for one user (depending on their settings).
- **Calendar Integration (future idea):** Possibly offer adding the upcoming ACT test date to their calendar or scheduling reminders there. Not required, but could be a nice integration (iCal link in email).
- **A/B Testing:** The team might experiment with different email content or timing. The system should allow tweaks easily (template editing as part of admin) to refine approach based on open rates and engagement.

Through well-thought-out notifications, the platform maintains a presence in the student’s routine, guiding them gently towards consistent practice and keeping them informed of important events, thereby enhancing the overall experience and outcomes.

## Payment and Subscription Module

The Payment and Subscription module manages user access through paid plans. This includes handling subscription sign-up, payment processing, plan management (upgrades/downgrades), and ensuring that only subscribed (or trial) users can access premium features. It also deals with free trial periods and possibly different tiers of service. Security and compliance (like PCI DSS via using a payment gateway) are paramount here.

### Key Features and Functional Requirements

- **Subscription Plans and Pricing:** Define the available plans:

  - For example: _Free Trial_ (full access for 7 days), _Monthly Subscription_ (paid monthly), _Annual Subscription_ (paid yearly at a discount), maybe _Institutional License_ (for bulk, though that might be handled offline).
  - Possibly different tiers: e.g., Basic (access to content and tests) vs Premium (includes AI tutor, extra coaching). But initially maybe one paid tier with all features.
  - The system should allow easily adding or modifying plans (though plan changes likely done infrequently and mostly in code or via payment platform configuration).

- **Free Trial Management:**

  - New users get X days of free access upon registration (no card required upfront or maybe card required but not charged until trial ends, depending on business model).
  - The system tracks trial start and end. When trial is nearing its end, notify user (as discussed in notifications).
  - If trial ends and user hasn’t subscribed, handle the transition: possibly restrict access (“Your trial has ended – please subscribe to continue”) with a prompt to choose a plan. Ensure no sudden loss of user data; their progress stays saved behind the paywall.

- **Payment Processing:**

  - Integrate with a secure payment gateway (e.g., Stripe, Braintree, etc.) to handle credit/debit card transactions. Ideally use their hosted fields or APIs so that sensitive card info never touches our servers (tokenization).
  - Allow user to enter payment details on a secure form (with validation for number, expiry, CVV, etc.). Support major card brands; possibly also PayPal or other methods if needed (not initially required).
  - Process subscription purchase in real-time: if card is approved, activate their subscription immediately.
  - Handle declines gracefully: if payment fails, show error and let user retry with different card.
  - Ensure compliance: use HTTPS, meet PCI compliance by not storing raw card data (just store a token or last4 + expiration for display).

- **Subscription Activation and Access Control:**

  - Upon successful payment, mark the user account as subscribed with an expiry or next billing date.
  - The system’s other modules should check subscription status for gated content: e.g., if unsubscribed and trial over, block access to practice tests or something. (If some content is free and others premium, enforce accordingly, though likely most features beyond maybe an initial diagnostic are premium).
  - Immediately unlock any previously restricted features after payment.

- **Recurring Billing:**

  - Automatically charge the user’s saved payment method at each interval (monthly/yearly). This will usually be done via the payment gateway’s subscription features or our scheduled job.
  - If a charge succeeds, extend their access another period and send receipt.
  - If a charge fails (card expired, insufficient funds), notify the user and give a grace period. Possibly retry charge after a few days. If still failing after X days, pause/cancel subscription.
  - Provide a grace period after renewal failure so user can update card without losing access immediately (e.g., 7-day grace).

- **Upgrade/Downgrade Plan:**

  - If multiple tiers, allow switching. E.g., Monthly to Annual (upgrade): charge pro-rated amount or start new period after crediting remaining days. Many systems just start new period, or for simplicity maybe wait until end of current period then switch – depends on approach.
  - Downgrade (if tiers present): schedule the downgrade for the next billing cycle to avoid partial refunds, or do immediate with proration if needed.
  - If adding an “Institution/Group plan” later, likely handled via sales rather than self-serve, but could integrate code if needed.

- **Cancellation:**

  - Users should be able to cancel auto-renew at any time (via account settings). When canceled, keep service until the period ends, then do not renew (i.e., set subscription to not renew).
  - Alternatively, allow immediate cancellation and optionally partial refund if within refund window – but usually simpler to let it run out.
  - Provide feedback flow on cancel (ask why, maybe offer discount to stay).
  - After cancellation, ensure their account reverts to free status at end date and they lose access to premium content then (but keep their data saved so if they resubscribe, it’s all there).

- **Refunds:** If a user requests a refund and it’s within policy (say 7 days of charge), admins should be able to issue via admin dashboard. The system should mark that subscription as refunded/cancelled accordingly. (This is more admin side, but system should handle if a user is refunded and cancelled).
- **Payment Receipts and Invoices:**

  - Email receipts for each payment (with amount, date, last4 of card, etc.).
  - Option to download invoice PDFs from account billing section (especially for annual or higher-cost transactions where they might need it for records).

- **Account Billing Management:** A section in user’s account (perhaps “Billing”):

  - Show current plan, next billing date and amount.
  - If in trial, show trial remaining time and maybe a convert button.
  - Allow entering/updating payment info securely.
  - Allow canceling subscription (with confirm).
  - If applicable, allow reactivating a canceled subscription before it expires.
  - Show billing history: list of past payments (date, amount, method).
  - If using discount codes, show that info (like “Student50 Discount Applied”).

- **Promo/Discount Code Support:**

  - On the payment form, a field to enter a promo code (if provided via marketing). Validate against a list (admin should manage codes: e.g., “SUMMER21 gives 20% off first 3 months”).
  - If valid, adjust price displayed and note terms (e.g., “Promo applied: 20% off”). Then process accordingly (for recurring, may apply to first payment or multiple depending on promotion design).

- **Multiple Currencies (Future):** likely not needed if focusing US. But if international, might allow selecting currency or auto by location (requires currency support in gateway and price points).
- **Group/Family Accounts (Future):**

  - Perhaps in future, a parent could pay and have a couple child accounts under them. Not in current scope, but ensure data model could extend (like linking child accounts to a payer).
  - For now, assume one subscription per user.

- **Security and Compliance:**

  - As mentioned, do not store sensitive card data on our servers – use gateway tokenization.
  - Store minimal info: maybe last4, card brand, expiration (to show user “using Visa ending 1234, exp 12/24”).
  - Protect that info as personal data.
  - Ensure the payments and financial records are secured and only accessible to authorized (like the user themselves and certain admins).
  - If handling any EU payments, comply with Strong Customer Authentication (SCA) – Stripe handles this typically by popping 3D Secure flow if needed.
  - If user deletes account and requests data deletion, ensure we handle subscription accordingly (cancel it, and possibly maintain transactional records as needed for financial laws but disassociate personal info if required).
  - Privacy: do not share payment info. Also, any integration with banks etc is through gateway.

- **Testing and Fail-safes:** Simulate various scenarios (card decline, etc.) to ensure flows are smooth.
- **Institutional Sales (Out of Band):** The system might support a different path where an institution license is applied to many accounts (like admin toggles them as paid via a code or domain-based access). Not in user self-serve scope now, but something to consider in design.

#### User Stories (Payment & Subscription)

- _As a new user,_ I want to sign up for a **free trial** without entering payment info, so I can evaluate the platform before committing to a purchase.
- _As a trial user,_ I want to receive a **reminder before my trial ends** so I’m not caught off guard and can decide whether to subscribe.
- _As a user,_ I want the process of **subscribing with my credit card** to be quick, easy, and secure, so I can gain full access without worry.
- _As a subscriber,_ I want to be able to **update my credit card info** if it changes (before my next billing) so that my subscription continues without interruption.
- _As a subscriber,_ I want to know **when I will be charged and how much**, and receive a confirmation or receipt each time, so I have full transparency.
- _As a user,_ I want to have the freedom to **cancel my subscription easily online** without having to call or email, so I feel in control and trust the service.
- _As a user,_ I’d appreciate **prorated upgrades** if I switch from monthly to annual, or some fair handling, so I don’t feel I’m paying double.
- _As a cost-conscious user,_ if I get a **promo code**, I want to apply it and see the discount reflected before I pay, so I’m confident I got the deal.
- _As an admin/support rep,_ I want to be notified if a user’s payment fails and the system has retried, so we can reach out or assist if needed.
- _As an admin,_ I want to ensure the system **does not allow access** to premium features for non-paying users after trial, to protect our revenue (while still being user-friendly in guiding them to subscribe).
- _As a parent (if relevant),_ I might want to pay for my child’s account – so the system should accommodate that scenario gracefully (perhaps via the child’s login or a parent account handling payment).
- _As a user,_ I want the **billing page** to show me everything about my subscription (plan, next charge, ability to cancel) clearly, to reduce any confusion or anxiety.
- _As a user concerned about security,_ I want assurance that my payment details are **handled securely (PCI compliant)** and not stored unsafely by the platform.

#### Example Use Case: From Trial to Subscription Management

1. **Free Trial Start:** Jane signs up for the platform. During sign-up, she sees “Start your 7-day free trial – no credit card required.” She registers and immediately has access to all features, marked as “Trial (ends on \[date])” internally.
2. **Trial Reminder:** On day 5 of her trial, the system sends Jane an email: “Your trial ends in 2 days – don’t lose your progress! Choose a plan now to continue seamlessly.” Jane decides she likes the platform and clicks the link to subscribe.
3. **Choosing Plan:** Jane is presented with pricing options: Monthly \$30/mo, or Annual \$300/year (save 20%). She chooses Annual (for the discount).
4. **Payment Input:** The site asks for her credit card info. She enters her card number, exp, CVC, name, possibly billing zip code. She also enters a promo code “SCHOOL20” that she got from a counselor for 20% off first month/year. The system validates it: “Code applied: 20% off first payment.” So her \$300 annual will charge \$240 (20% off) now, and future renewals at normal \$300 (if code only applies to first term).
5. **Confirmation:** She clicks “Subscribe”. The payment processes (via Stripe). It’s successful. She sees an on-screen confirmation: “Thank you for subscribing! Your next billing date is one year from now on \[date].” Her account now is marked “Premium Annual – active”.
6. **Access and Receipt:** She already had access (trial), but now it won’t cut off. She receives an email receipt detailing the charge \$240 (with promo) for 1 year Premium, paid via Visa \*\*\*\*1234.
7. **Mid-cycle Update Card:** Six months later, Jane realizes her card on file will expire. She goes to her Billing settings. She sees “Card on file: Visa ending 1234, exp 09/2023”. She clicks “Update Payment Method”. She enters a new card. The system verifies it (maybe a \$0 auth) and updates. She gets a confirmation email of card change (for security).
8. **Upgrade/Downgrade Example:** If there were multiple tiers (say a Basic and a Premium with tutoring), this is where she might upgrade if she wanted extra services. But in our simple scenario, skip.
9. **Cancellation Flow:** After the year, imagine Jane’s test is done and she doesn’t need another year. She goes to Billing and clicks “Cancel Subscription”. The system perhaps asks “We’re sorry to see you go – any feedback?” She gives a reason like “No longer needed, finished test”. She confirms cancel. The interface now shows “Your subscription will not renew. You have access until \[original end date]. Reactivate anytime.” She also gets an email confirming cancellation, and maybe an offer “If you change your mind within 30 days, you can renew without losing your data.”
10. **Renewal Attempt and Failure:** Alternatively, if Jane didn’t cancel, at the one-year mark the system tries to charge her card \$300. If it succeeds, new year active, she gets a receipt. If it fails (say her card was expired and she hadn’t updated), the system emails: “We couldn’t renew your subscription. Please update your payment info within 7 days to retain access.” Meanwhile, maybe her account is in grace period (still active for those 7 days). She updates card, system retries (or she manually triggers retry by clicking “Pay now”), and then it succeeds, maintaining access.
11. **Refund Scenario:** If Jane realized two weeks into renewal that she no longer needs it, she might contact support. An admin then uses the admin dashboard to issue a prorated refund or full refund (depending on policy) and cancel the sub. The system would then immediately mark her as free user. She may get a “We’ve processed your refund of \$X, your subscription has been canceled” email.
12. **Institution Bulk (future):** Not directly shown to Jane, but e.g., if her school bought a license, possibly she would have a coupon or code to redeem for free access rather than entering payment at all. She could apply that code on sign-up and skip payment (the system would mark her as paid via institution until some expiration). This is a special case workflow to consider eventually.

#### UI/UX Considerations

- **Plan Selection UI:** Make it clear what each plan offers (if multiple). Possibly highlight the recommended or best value plan. Use simple language (“Billed monthly” vs “Billed annually (save 20%)”). Ensure currency sign and amount are prominent.
- **Payment Form UX:** Should be clean and trustworthy:

  - Show security assurances (“Secure Payment” badge, maybe “Powered by \[Gateway]”).
  - If using Stripe Elements, it will handle formatting/validation nicely. Otherwise ensure realtime validation (card number format, expiration not past, CVV length).
  - Accepting only credit/debit at first is fine; if needed, consider PayPal or others if user base demands.

- **Promo Code Field:** This should apply without reloading page and show updated price. Indicate if code invalid with message.
- **Price Calculation:** If proration or partial charges occur (like upgrade mid-cycle), explain clearly what will happen (“You will be charged \$X now, and next billing on Y date will be at new rate Z.”).
- **Trial messaging:** When trial is active, many pages might remind “X days left in trial.” And on locked features (if trial had limitations, though likely full access trial).
- **Graceful lockout:** If trial or sub expired, the next time user tries a premium feature, show a paywall screen: “Your trial has ended. To continue using \[Feature], please subscribe.” Provide link to pricing page.
- **Account/Billing Page:** This is crucial for trust:

  - Clearly list current status: “Active – will renew on \[date] for $\[amount]” or “Canceled – will end on \[date]” or “Trial – ends on \[date]”.
  - Button for “Manage Subscription” or separate buttons: Update Card, Cancel Subscription.
  - Possibly link to contact support for billing help.

- **Mobile responsiveness:** Payment page should work on mobile since some may subscribe from their phone (especially if using app with webview or linking out).
- **Notifications in app:** If a payment fails or subscription lapses while they’re using the app, handle it: e.g., show a banner “Payment required to continue” etc.
- **Error handling:** If gateway is down or internet glitch, show an error and do not charge twice accidentally. Also, disable subscribe button after click to avoid double submit.
- **Security UI cues:** Lock icons, “https\://“ visible, etc., to reassure.
- **Privacy:** When displaying credit card info in Billing, mask all but last4. If collecting billing address (not strictly needed unless dealing with AVS or taxes), keep it minimal and protected.
- **Tax Handling:** If required to charge tax (like VAT in some countries or sales tax in some states for digital goods), that complicates pricing display (need to possibly show tax on checkout or include it). For simplicity, maybe avoid initial, but plan should be open to adding if expansion.
- **Extensibility:** If new products or services are added (like one-on-one tutoring sessions for a fee, or premium plans), ensure the payment system can handle one-time charges or multiple product SKUs. Currently just subscription one SKU likely.
- **Cancellations:** Ensure after cancel, the user isn’t charged. Also if they resubscribe later, the process works (could be immediate new charge or start at end of last period, depending).
- **Data retention:** If subscription lapses, do not delete their data. Keep their progress so if they resubscribe, they pick up where left off. (This should be default, just ensuring we think it through.)
- **Information:** Provide maybe a FAQ link about billing and subscription on the page, covering common questions (cancel anytime, refund policy, etc.), to reduce support issues.
- **Email Confirmations:** Every critical action should trigger an email: purchase receipt, card update (security notice), cancellation (confirmation so they have it in writing), renewal upcoming (maybe send 3 days before annual renewal as courtesy).
- **Admin oversight:** If an error happens in billing (like our server can’t confirm a payment but user got charged), have a way to reconcile (likely rare if using robust API, but ensure no user is stuck in limbo).
- **Trial abuse prevention:** Consider limiting one trial per user (or per email). Possibly by email uniqueness (could be circumvented by new email). If that’s a concern, might require card for trial to avoid abuse, but that also adds friction. Business decision beyond PRD scope, but system should handle whichever way decided.
- **Edge Cases:** e.g., user signs up, immediately subscribes (skips trial essentially) – allowed. Or user cancels during trial (just let trial run out).
- **Support for promotional flows:** e.g., “Refer a friend get 1 week free” – not initially needed, but can be layered with adjustments to subscription timeline.

The Payment & Subscription module ensures a seamless transition from interested user to paying customer, maintaining trust through transparency and control, while safeguarding revenue by properly gating access.

## Mobile App Interface Overview

The Mobile App Interface is an extension of the platform for smartphones (and possibly tablets). While the core functionality mirrors the web (student portal, practice engine, content, AI tutor), the mobile app must present these in a mobile-optimized way and leverage mobile-specific features (like push notifications, offline access). This overview highlights how the mobile experience is tailored and any differences or additional considerations.

### Platform and Design

- The mobile app will be available for **iOS and Android**. It could be built natively for each or using a cross-platform framework (React Native, Flutter, etc.), but that’s an implementation choice. For this PRD, we focus on capabilities.
- The app should maintain consistent branding and general look & feel with the web, but use native mobile UI patterns (bottom navigation bars, swipe gestures, etc., as appropriate).
- It should support the same user account system – users log in with the same credentials and see their synced data (tests, progress) seamlessly.

### Key Features on Mobile

All major modules should be accessible on mobile, potentially with slight modifications:

- **Student Dashboard:** A simplified dashboard for small screen:

  - Top section might greet user and show an at-a-glance stat (like “Next ACT: 30 days” or “Last score: 26”).
  - Key actions as big buttons: “Take Practice Test”, “Practice a Section”, “View Lessons”, “Chat with Tutor”.
  - Possibly a carousel or tabs for recent scores, upcoming tasks, etc., in a compact form.

- **Practice Test Engine:**

  - Likely one question per screen (swipe or tap Next to move).
  - Timer at top.
  - If reading passage, maybe a toggle or a way to view passage full-screen and then return to questions, since side-by-side is tough on small screen.
  - Ensure scrolling is handled (e.g., some questions might need scrolling if long).
  - Use native controls for selecting answers (perhaps custom radio buttons big enough to tap).
  - Keep the experience focused (maybe auto-hide status bar for full-screen immersion).
  - Possibly allow landscape orientation for certain sections (landscape might show passage and question side by side on a plus-sized phone, or just give more space for reading).
  - If internet drops, app should allow continuing and sync results later.

- **Learning Content:**

  - Videos: use the native video player capabilities. Allow full-screen playback in landscape.
  - Quizzes: similar to practice questions; possibly more immediate feedback if in practice mode.
  - Text lessons: scrollable content, ensure formatting is responsive. Possibly enable pinch-zoom on images or text if needed.
  - Download option: maybe allow downloading videos for offline viewing (with DRM concerns, but possible via storing encrypted and restricting to app).

- **AI Tutor Chat:**

  - A chat interface using typical messaging UI. On mobile, maybe more frequently used, as it’s like texting a tutor.
  - Support voice input (user could tap a mic to dictate a question) or even voice output (text-to-speech for answers) – optional but mobile makes these feasible.
  - Possibly allow attaching a photo of a problem (user snaps a picture of a math problem in their workbook and sends to AI). If we can process that via OCR, AI could help – advanced, but a known use-case on mobile (like Photomath style). Even if not immediate, design the system to potentially accommodate that.

- **Offline Mode:**

  - At least partial functionality offline. E.g., if a user is on a train with no internet:

    - They should be able to open and review downloaded content (videos, notes).
    - Possibly take a practice test offline – store the result locally and sync to server when back online (ensuring no cheating issues, but since it’s practice it’s fine).
    - The app should detect offline state and inform which features are limited (“AI tutor requires internet”, obviously that won’t work offline; but tests and lessons could).
    - Use local storage for caching recent data like their progress to display.

- **Push Notifications:**

  - As covered in Notifications, the app will receive pushes for reminders and updates. The app should route these to the appropriate screen when tapped (deep linking).
  - E.g., “Practice reminder” push takes them to a quick quiz or dashboard; “Score ready” push opens the results of that test.

- **Performance:**

  - App should be snappy; heavy computations (scoring test) mostly done on back-end, so app just displays results.
  - Use background threads for any processing to keep UI smooth.
  - If any heavy content (like loading a big list of questions), use progressive loading or loading spinners.

- **Device Compatibility:**

  - Should work on common devices (e.g., iPhone 8 or later, Android phones with reasonable specs, likely support Android 8+ and iOS 13+ for broad coverage).
  - Adapt layout for tablet vs phone – maybe on tablets, can show more at once (like an iPad could show a whole section’s questions list on side).

- **Security:**

  - Implement secure local storage for any cached personal data. Possibly encrypt sensitive data at rest on device (some frameworks do automatically).
  - Ensure the API tokens or credentials used by the app are stored securely (keystore, keychain).
  - Protect against someone extracting the app data (though if they did, it’s mostly just their own content).
  - If user sets a PIN or biometric for app (could be a feature to quickly log in via fingerprint/FaceID instead of password each time).
  - The app should require login (maybe offer “remember me” to keep user logged in, but with secure token refresh).
  - Data transfer always over HTTPS.
  - If the user is offline and has test data unsynced, ensure it syncs to correct account upon reconnection and not lost or mis-sent.

- **Updates:**

  - The app should handle version updates gracefully. If a new version is required (because API changed), notify user to update via store.
  - Possibly an in-app update prompt if critical.

- **Feature Parity Gaps:**

  - Some admin features obviously won’t be in mobile app (we don’t expect admins to use the mobile app for content uploading; admin stays web).
  - The mobile app is purely student-facing (and maybe teacher facing if we make a teacher view, but likely focus on students).
  - If there’s any feature we decide not to put in app (though ideally all student features are there), clarify it. For instance, maybe complex analytics graphs might be simplified on mobile or omitted if not fitting – but we can still show key metrics.

- **UX Differences:**

  - Navigation likely via a bottom nav or a hamburger menu. Possibly bottom nav with icons: Home, Practice, Lessons, Tutor, Profile.
  - The “Home” might combine dashboard and analytics succinctly.
  - Use native UI elements: e.g., pull-to-refresh on certain screens to sync data, swipe gestures (maybe swipe between question flashcards or swiping to navigate).
  - When a test is in progress, perhaps lock orientation to prevent weird jumps (or at least handle orientation changes gracefully by saving state).
  - Possibly incorporate haptic feedback on certain events (like a subtle vibration when time is up, if not intrusive).

- **Testing on Mobile:**

  - The app needs thorough QA on devices to ensure layouts work and that things like the timer keep running even if phone goes to sleep (if allowed; might have to prevent sleep during a test).
  - Also ensure memory usage is not too high (especially if loading many images for science graphs).

- **Downloads:** If enabling offline content, provide a screen to manage downloads (like “Downloaded Videos” with the size they take, ability to delete downloads to free space).
- **App Size:** Keep the app reasonably sized by not packaging too many large files. Content can be loaded from network or downloaded as needed rather than bundling all videos, etc.
- **User Engagement:** Possibly consider mobile-specific engagement features:

  - Maybe a daily question push: “Daily Challenge: try this ACT question!” where user can answer right from notification or quick in app for a bit of gamification. This could keep them coming back daily.
  - The mobile format is great for micro-practice (a couple questions on the go).
  - Ensure the app is inviting for those quick sessions, not just full tests.

- **Integration with Phone Functions:** Could allow calendar integration (add official test date to calendar with one tap), or share progress (share to social that “I scored 30 on ACT practice – yay!”) if appropriate.

  - Social sharing might not be desired by many, but at least data should be portable if they want to share with parent by message.

- **Accessibility:**

  - Support iOS VoiceOver and Android TalkBack for visually impaired (this is challenging for graphs but at least reading text).
  - Ensure button labels and alt text for any icons in app.

#### User Stories (Mobile App)

- _As a student,_ I want to use the platform on my **smartphone** so I can study and practice even when I’m away from my computer (like on the bus or during a lunch break).
- _As a student,_ I want the mobile app to send me **push notifications** for important things (reminders, results), as those are more noticeable than emails for me.
- _As a student,_ I want to be able to **take a practice quiz or review flashcards on my phone offline**, for example when I don’t have internet, so I can make use of downtime anywhere.
- _As a student,_ I want the app UI to be simple and not require a lot of typing (aside from answers), leveraging mobile conventions, so that it’s easy to navigate on a small screen.
- _As a student,_ I want to **watch lesson videos on my phone** and possibly download them beforehand, so I can learn on the go without streaming issues.
- _As a student,_ if I think of a question while out, I want to **ask the AI tutor on my phone** right away, like texting a friend, so I get instant help.
- _As a student with limited data,_ I want the app to **only use heavy data (videos) when on Wi-Fi** or allow me to choose, so I don’t burn through my data plan (maybe a setting to only stream on Wi-Fi).
- _As a student,_ I expect the app to **sync** with the website – if I start a test on my phone and finish it, I want to see that result on the web later, and vice versa.
- _As a student,_ I sometimes prefer studying on my tablet; I want the app to use the bigger screen effectively (not just a blown-up phone UI).
- _As an instructor (if app allows),_ I want to see my students’ progress on the app too and maybe send them a quick message or nudge through it.
- _As a user,_ I want the mobile app to be **stable and not crash**, especially during a long practice test, to preserve my effort.

#### Example Use Case: A Day with the Mobile App

Morning: The student receives a push notification on their phone at 8am: “Good morning! 15 days until your ACT. Try a quick 5-question quiz now to warm up.” They tap it, the app opens directly to a “Daily Quiz” of 5 questions. They answer them (the app gives immediate feedback after each since it’s in practice mode). After finishing, it says “Great job, you got 4/5 correct. Come back tomorrow for another daily quiz!”

Afternoon: On the bus ride home, the student opens the app to watch a video lesson. They go to “Lessons”, find “Punctuation Basics” video. They hit download while on school Wi-Fi earlier, so now it’s available offline. They watch the video with headphones. There’s a quiz attached; they don’t have internet but since it was downloaded, they can still take it and the app will save the results. They get 8/10 correct. The app marks the lesson completed. Once they get home and reconnect to Wi-Fi, the app syncs that quiz result to their account (so later on web, it shows done).

Evening: The student is doing homework and stuck on a math problem. They open the app and use the AI Tutor chat: They type (or speak) the problem into chat. The AI responds with an explanation. They follow up with another question, and so on. This conversational help via phone is very handy.

Night: The student decides to take a full practice test before bed. They plug in their phone (since it might take \~2.5 hours with writing) or maybe just do sections separately if that’s long for mobile. They start an ACT test on the app. The app advises to find a quiet spot and perhaps recommends landscape orientation for best experience. They proceed through the exam; the app keeps the screen awake and timer visible. They complete all sections. Upon submission, since they’re online, it immediately grades it. They see their scores on the phone. Because it’s late, they decide to not analyze deeply now.

Next morning, on the computer, they check the detailed analytics of that test on the web. All the data was synced from the mobile attempt.

#### UI/UX Considerations (Mobile specifics)

- **Navigation:** Use a tab bar or clear navigation. Possibly:

  - Home (dashboard)
  - Practice (where they choose full test, section, quiz)
  - Lessons (content library)
  - Tutor (AI chat)
  - Profile (progress/ settings)
    Or combine some logically. Keep max 5 tabs for clarity.

- **State Sync:** The app should reflect any actions done elsewhere after a refresh (pull down to refresh or automatic on open).
- **Onboarding in App:** Maybe a brief tutorial overlay for first-time app users to show how to navigate or where things are (since can differ from web).
- **Touch Targets:** All buttons, checkboxes must be finger-friendly (Apple HIG says at least 44px).
- **Font Size:** Ensure text is readable on small screens (avoid tiny font especially in explanations; allow pinch zoom in content).
- **Color and Contrast:** Use high-contrast colors for outdoor use etc. Possibly provide a dark mode for those who study at night (nice on eyes).
- **Sound/Vibration:** Optionally, a ticking sound for last 5 seconds of a timer? Probably not, might add stress; maybe just a vibration when time’s up if app in background.
- **Memory usage:** If user is doing a full test, ensure app doesn’t eat memory that would cause OS to kill it in background if they switch temporarily. Possibly warn them not to leave app during a timed test (like "your test is in progress, don’t close the app or you may lose progress").
- **Crash Recovery:** If app did crash mid-test, it should try to recover answers (maybe autosave partial answers locally every few minutes).
- **User Feedback Collection:** Provide a way to report bugs or feedback via the app (maybe under settings “Report a Problem” that emails support).
- **Continuous Improvement:** Use analytics to see how users use the app differently (maybe more likely to do short quizzes vs full tests) and optimize accordingly.
- **Store Presence:** The app’s listing on App Store/Play Store should align with our features and be appealing (this is more marketing but relevant to adoption).
- **Login Persistence:** Keep users logged in on app unless they log out (with secure token refreshes) so that it’s quick to open and start using without frequent re-login.
- **Cross-platform quirks:** e.g., handle Android back button (should navigate inside app, not just exit abruptly).
- **Testing on Real Devices:** Emphasize this to find any layout issues or performance bottlenecks.

The mobile app ensures students have a convenient, accessible way to integrate ACT prep into their daily lives, capturing small pockets of time and making studying more flexible and personalized (like using the AI tutor in a chat-like fashion). By aligning closely with the web features but optimizing for touch and mobility, it can significantly boost user engagement and consistency in prep.

## API Architecture for External Integrations

The platform will expose an **Application Programming Interface (API)** to allow external systems and developers to integrate with its functionalities. This includes the mobile app (which is essentially an external client to the backend API), any partner integrations (like school systems or third-party education apps), and possibly public API access if the product decides to open certain features to external developers. Designing a robust, secure API ensures the platform’s data and functionality can extend beyond the core web interface.

### Architectural Style and Technology

- The API will likely be a **RESTful JSON API** over HTTPS, given its wide familiarity and ease of use. Endpoints for resources like `/users`, `/tests`, `/results`, etc.
- Alternatively or additionally, we could consider **GraphQL** for more flexible queries from clients, but that adds complexity. Likely stick to REST for initial design simplicity.
- Use consistent base URL (e.g., `api.platform.com/v1/`).
- Use standard HTTP verbs: GET (fetch data), POST (create), PUT/PATCH (update), DELETE (remove).
- Response in JSON format; requests with JSON body for create/update.
- Use appropriate response codes (200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found, etc.) to communicate status.

### API for Mobile App

The mobile app will use the API extensively:

- **Authentication:** likely via OAuth2 with token (perhaps a JWT) or a session token system. E.g., mobile logs in via `/auth/login` with credentials, gets an access token to include in headers for subsequent requests.
- All the features:

  - Fetch user profile `/users/me`
  - Fetch content lists `/lessons`, specific lesson `/lessons/{id}`
  - Fetch quizzes or test definitions `/tests/{id}`
  - Submit test results `/results` (POST with answers)
  - Chat with AI might use a different channel (maybe a WebSocket or long-poll endpoint for real-time, or send question to an AI endpoint and get response).
  - Retrieve analytics data `/analytics/me` (for student’s stats)
  - etc.

- The API should be designed such that the mobile app can do everything needed without hacks.
- Also ensure the API is efficient to minimize data transfer on mobile (e.g., bundle needed info in one call when possible, use pagination for big lists).

### External Integrations

Potential integration scenarios:

- **LMS Integration (Learning Tools Interoperability - LTI):** A school might want to integrate the platform into their LMS like Canvas or Blackboard. LTI support would allow one-click sign-on and launching the platform for students and returning scores back. That’s a specialized API/protocol (LTI 1.3) that could be considered. It involves a different kind of integration than simple REST. If this market is aimed (schools), including LTI in roadmap is wise. But if direct consumer, not needed initially.
- **Data Export:** Schools might want to pull data into their systems. So an API that allows authorized requests for, say, “Get all results for students X, Y, Z” or “Get all students and their latest scores in class ABC.”
- **Single Sign-On (SSO):** API endpoints to support SSO (SAML or OAuth login from Google, etc.). Possibly allow students to sign in with Google – for that, we integrate Google OAuth on front-end and just accept Google token to our API for account creation or login. This is more internal but part of integration concept (with identity providers).
- **Public API (for partnerships or developer use):** We might allow external developers (with API keys) to access certain data (with user permission) to create add-ons. For instance, a tutoring company could use the API to fetch their students’ progress and incorporate into their own dashboard.
- **Embed Content:** Perhaps an external site might embed our practice questions via API calls – probably not priority unless we white-label.
- **Connect with other tools:** e.g., a calendar integration could use an API to push an event to Google Calendar (though that’s more our integration outward).
- The API should be comprehensive enough to cover retrieving content data, posting user-generated data (answers, notes), retrieving analytics, and managing users (to some extent, though user creation likely via our interface).
- Possibly an API for creating users in bulk (if a school uses an SIS integration to create accounts on our platform automatically) – that might be a private admin API or done via CSV import rather than open API.

### API Security

- **Authentication & Authorization:**

  - Use OAuth 2.0 protocol for external API access. For example:

    - Mobile app uses Resource Owner Password Grant (or better, a proper login flow with token).
    - External integrations could use Client Credentials for server-to-server (like a school with an API key and secret gets a token to access their data).
    - Or use API keys for simple cases (but OAuth tokens are more standard).

  - JWT tokens can be used as access tokens for stateless auth on API calls. The server must validate these on each request (signature, expiration, etc.).

- **Scope & Permissions:**

  - Ensure tokens are scoped: e.g., a teacher’s token can only access their students. A student’s token can only access their own data.
  - Possibly implement roles in API responses: an admin token can GET any user’s data; a student token only `me`.
  - External API keys given to partners should only allow their subset (like an institution only pulling their students).

- **Rate Limiting:**

  - Implement rate limits to prevent abuse or accidental overload. E.g., limit to X requests per minute per IP or per token. (Make exceptions for internal mobile app if needed, but generally design mobile not to spam).

- **Input Validation & Sanitization:**

  - All API inputs need robust validation – since external systems might send unexpected data. Use standard libraries to avoid injection attacks (though JSON not directly prone to SQL injection if using parameterized queries, but be cautious).

- **Versioning:**

  - Prefix with `/v1/` so if changes needed, we can introduce `/v2/` without breaking old clients.

- **CORS:**

  - If web apps from other origins (maybe not needed, but if someone wants to make a custom dashboard and call our API from browser, we might allow with proper authentication).

- **Documentation:**

  - Provide API documentation (perhaps OpenAPI/Swagger spec) so integrators know how to use endpoints. This is important if we expose publicly or to partners. Possibly even an API explorer or Postman collection.

- **Webhooks:**

  - Optionally, support webhooks for certain events. E.g., a school’s system might register a webhook URL to get notified when a student completes a test (with the result payload). This pushes data rather than them polling. Only if demand arises, but good to note.

- **Use Cases for API:**

  - A school’s **SIS** wants to sync roster and scores: They call our API to create accounts for their students (or we import), and they call our API weekly to get new scores to put into their gradebook.
  - A third-party **analytics tool** might request data (with permission) to run deeper analysis on outcomes.
  - The **mobile app** as noted is a key API consumer.

- **Microservices and API gateway:**

  - On the backend architecture, if we break into microservices, the API Gateway will unify them. For this document, assume one unified API service for simplicity.
  - We might have separate internal APIs (between services) not exposed externally.

- **Testing & Stability:**

  - The API must be thoroughly tested because mobile and other systems depend on it. Changes to API need backward compatibility or version bump to not break the mobile app if it’s not updated simultaneously.
  - Maintain stable contracts or use feature flags to coordinate changes.

- **Performance:**

  - Design endpoints to minimize number of calls needed. For mobile, one call might fetch multiple related data (if not too heavy) to reduce chattiness. Or use GraphQL to let client fetch exactly what it wants in one go.
  - Use caching for repeated GET requests where appropriate (like content that doesn’t change often could be CDN cached).
  - Use pagination for any large lists (like if listing all questions – though normally we wouldn't do that in client).

- **Data Filtering:**

  - Allow query parameters to filter results (e.g., GET /results?since=2025-01-01 for results after a date).
  - In a teacher context: GET /results?classId=123 to get that class’s results (ensuring teacher’s token is tied to class).

- **Integration Onboarding:**

  - If we open API to third parties, we need a developer portal or at least a process to obtain API credentials. Possibly at first it's manual with our admin issuing them for partner schools.
  - Provide sample code or SDKs if resources allow, to simplify integration (not necessary in PRD, but thinking ahead).

- **Privacy & Data Sharing:**

  - Only share student data with authorized parties. E.g., if an external app wants to fetch a student’s data, that student (or their guardian) should have granted permission. Possibly via OAuth 2.0 Authorization Code flow where user authorizes the third-party.
  - Or for institutional use, that’s covered by FERPA school official designation, etc., but ensure there's an agreement and technical controls.

#### User Stories (API & Integrations)

- _As a mobile app developer (internal),_ I need a comprehensive **API** to fetch and update all necessary data (users, content, answers, etc.), so I can build the mobile app independently of the web codebase.
- _As an IT administrator at a school,_ I want to **integrate the platform with our school systems**, such as automating account creation and pulling student scores into our gradebook, to streamline adoption and tracking.
- _As an external developer,_ I might want to build a **companion app or script** (with permission) that uses the platform’s data (for example, a custom analysis dashboard). I need secure API access with clear documentation to do this.
- _As a teacher,_ I'd love it if our existing LMS could **launch into this ACT platform seamlessly** and maybe even return scores. An LTI integration or SSO would save me and my students from multiple logins.
- _As a product manager,_ I want our platform to be **extensible**; offering an API means we can form partnerships (e.g., a college prep service might integrate our data) and it future-proofs our system for unforeseen uses.
- _As a security officer,_ I want to ensure that any external access to data via API is **secure and limited**, so no unauthorized entity can access student data and any keys/tokens can be revoked if needed.
- _As a parent,_ if I use an external educational tracking app, I might want to link my child's ACT prep progress to it. Through an API (with consent), such an app could retrieve my child’s progress data from this platform to show alongside other academic metrics.
- _As an admin,_ I want to ensure the **mobile app and the web** stay in sync via the API so that users have a consistent experience switching between devices.
- _As a developer using the API,_ I want clear **documentation** and examples, and a sandbox perhaps, so that integration is straightforward and I don’t have to guess how endpoints behave.

#### Example Use Case: School LMS Integration

A high school uses an LMS (Learning Management System) to manage all coursework. They want to integrate the ACT training platform for their junior class test prep:

1. **Single Sign-On:** The platform supports SSO via SAML or OAuth. The school’s LMS is configured to allow students to click a “ACT Prep Platform” link which uses SSO to log them into our platform without separate credentials. Behind the scenes, we’ve exchanged metadata with the school; when a student clicks, our platform’s API receives a SAML assertion with the student’s identity, finds or creates their account, and logs them in. This is not exactly a public API thing but an integration mechanism likely done through known standards (SAML/OIDC).

2. **Automatic Roster Sync:** The school’s IT uses our API to create accounts for all their students proactively. They have an API key for their organization. They run a script or use a connector that calls `POST /users` for each student (with name, email, etc.) and perhaps sets them all to belong to “Spring ACT Class 2025”. The API returns the created user IDs or any errors (like if user exists). For existing users, they might update them or just associate them with the class.

3. **Assign Tests via LMS:** The teacher in LMS creates an assignment “Take Practice Test 1”. Ideally, through LTI integration, that assignment launch can direct to a specific test on our platform for each student. If full LTI is implemented, when student finishes test, our platform calls back to LMS with a grade or completion. If not LTI, teacher can manually get results. But let's say advanced: Our system has an LTI Outcomes integration: after a test completes, we know the LMS assignment ID and we send the score via LTI API back to LMS gradebook.

4. **Data Pull for Reports:** At end of program, the school wants all data. They call our API with their admin credentials: `GET /analytics?classId=Spring2025` which returns JSON of each student’s latest scores or improvements. They use that to generate a report or feed into a district system.

5. **Ongoing Sync:** If a student leaves or joins, their system can call our API to deactivate or add accounts so things stay in sync.

Another scenario: A third-party educational app for students has a feature to track test prep across SAT/ACT from different sources. If we had a public API, a student could authenticate that app to access their scores from our platform. Through OAuth, the student would authorize, and then that app could call endpoints like `GET /results` for that student. We’d ensure scope is just that student’s data. This way, the student sees their ACT practice progress alongside other metrics in one place. This is analogous to something like allowing a fitness app to pull data from a wearable—here it's academic data.

#### API Endpoints Example (just a brief list to illustrate):

- `POST /auth/login` – returns token
- `POST /auth/oauth-token` – for OAuth token exchange
- `GET /users/me` – get logged-in user profile
- `PUT /users/me` – update profile (e.g., set test date)
- `GET /content/lessons` – list lessons (with optional filters e.g., subject=Math)
- `GET /content/lessons/{id}` – get a lesson detail (including perhaps a video URL or text content)
- `GET /practice/tests` – list available practice tests (IDs, names)
- `GET /practice/tests/{id}` – get test details (like questions, or maybe questions come one at a time via separate call to avoid huge payload)
- `POST /practice/tests/{id}/start` – initiate a test, maybe lock a session ID
- `POST /practice/tests/{id}/submit` – submit answers (or could be a generic `POST /results` linking to test ID)
- `GET /results/{id}` – retrieve a past test result (scores, answers, etc.)
- `GET /analytics/progress` – overall progress for current user (or if admin/teacher, maybe for multiple via parameters)
- `GET /class/{classId}/results` – (for teacher role) get aggregate or list of student results in a class
- `GET /notifications` – if wanting to fetch in-app notifications
- `POST /notes` – create a study note
- `GET /notes` – list notes (maybe by lesson, etc.)
- `POST /tutor/query` – send a question to AI tutor (then maybe use WebSocket to stream answer or poll for answer).
- `WS /tutor/chat` – a WebSocket endpoint for live tutor conversation.

And endpoints for admin maybe:

- `POST /users` (admin only, create user)
- `GET /users/{id}` (admin or that user)
- etc.

But those details can be refined in technical design; the PRD ensures we have the capabilities in mind.

#### UI/UX for API usage

The API itself is backend, but if we consider providing to third parties:

- Likely have a Developer section on our website with documentation.
- Possibly a UI in admin to create API credentials for an institution (like generate client ID/secret).
- Monitoring interface to see API usage might be internal.

Ensure that any integration doesn’t degrade user experience:

- e.g., if an LTI launch fails, show an error nicely rather than cryptic.
- If two systems update a user’s data simultaneously, have proper concurrency handling (maybe last write wins, or locks if needed to avoid conflict).
- If external apps create content or data (less likely, but imagine an admin bulk importer), ensure it doesn’t mess up consistency.

In summary, the API architecture provides the backbone for all non-web-client interactions (mobile and beyond) and positions the platform to collaborate in a broader ed-tech ecosystem, while maintaining strict security and data privacy controls.

---

## Security and Privacy Considerations

Security and privacy are critical given that the platform handles sensitive student data (personal information, educational records) and payment details. We must ensure **confidentiality, integrity, and availability** of data, and compliance with relevant regulations like **FERPA** (for educational records) and **GDPR** (for users’ personal data, especially if there are any users from the EU or simply as a best practice). Below are the main security requirements and privacy measures:

### Authentication & Authorization

- **User Authentication:**

  - Use secure methods for storing credentials: passwords hashed with a strong algorithm (bcrypt or Argon2). Never store plain-text passwords.
  - Support OAuth2 for mobile and potential third-party login flows. Possibly integrate social login options (Google, etc.) as alternate methods (these need careful linking to existing accounts).
  - Implement account lockout or CAPTCHA after a number of failed login attempts to prevent brute force.
  - Offer 2-Factor Authentication for users (especially admins) as an option for added security (not mandatory for students, but maybe option via authenticator app or SMS).

- **Session Management:**

  - Use secure cookies for web sessions (HTTPOnly, Secure, SameSite=strict). For API, use short-lived JWTs with refresh tokens.
  - Automatically expire sessions after period of inactivity (e.g., log out web user after say 2 hours of inactivity, configurable).
  - Provide logout endpoint that destroys session/token.

- **Role-Based Access Control (RBAC):**

  - Clearly define roles (Student, Teacher, Admin, etc.) and enforce in the backend which endpoints and data each can access.
  - For example, a student cannot access another student’s results; a teacher can only access their class; an admin can access needed data but those interfaces are protected behind admin auth.
  - In the code, every request should check the user’s role and ownership where applicable (e.g., if student requests /results/{id}, verify that result belongs to that student).

- **Admin Security:**

  - Require strong passwords and ideally 2FA for admin accounts (since they have broad access).
  - Keep an audit log of admin actions (content changes, user data changes, etc.) to trace any malicious or erroneous activity.
  - Limit admin portal access by network (if internal staff mostly in office, maybe restrict to known IPs or VPN – optional).

### Data Privacy and Compliance

- **FERPA Compliance:**

  - Treat student educational records (practice scores, progress) as confidential. Only share with authorized personnel:

    - Students themselves, their parents (if under 18 or if account is set to share with parent), and their teachers/school officials who have legitimate educational interest.
    - If a school uses the platform, we likely act as a “School Official” under FERPA, meaning we must use the data only for the purposes intended by the school and not redisclose unless allowed.

  - Provide data access rights: a student (or their parent if minor) can request to see the data we have on them. The platform should be able to export their data (scores, personal info) on request.
  - Provide data amendment rights: if a student/parent finds an error in their personal data, allow correction (e.g., contacting support to change name spelling, etc.).
  - No disclosure to third parties without consent: We won’t share student data with advertisers or such. Any analytics for internal use will be de-identified aggregate.
  - Security controls: encryption in transit and at rest for protected records, role-based access (already covered), and monitoring for unauthorized access.

- **GDPR Compliance:**

  - Even if primarily US, we aim to adhere:
  - **Consent:** Get explicit consent for data collection and processing at sign-up (terms of service and privacy policy acceptance).
  - **Data Minimization:** Collect only data needed for the service (e.g., we don’t need student’s home address, so we don’t ask).
  - **Right to Access:** As mentioned, users can request their data. We should have a process to provide a structured copy.
  - **Right to Erasure:** If a user asks to delete their account, we will delete their personal data from our systems (except any data we must keep for legal or financial reasons, like payment records).

    - The platform should implement an account deletion function (maybe via support or automated): this would remove personal identifying info and results from the active database. (Alternatively, anonymize results if needed for aggregated stats but remove link to user).

  - **Breach Notification:** Have an incident response plan. If a data breach occurs involving personal data, we must notify users and authorities within 72 hours as required.
  - **Privacy by Design:** Integrate privacy considerations from the start (which we are doing in these requirements). For instance, make sure any new features consider data exposure.
  - **Data Processing Agreement:** Use reputable sub-processors (hosting, email service, AI provider) and have agreements in place that they comply with GDPR, etc. Inform users of these in privacy policy.
  - **Opt-Out of Personalization:** Possibly allow users to opt-out of certain data uses like AI personalization if they are uncomfortable (as hinted by FERPA guidelines).

- **COPPA (Children’s Online Privacy Protection Act):**

  - If any users <13 sign up individually, we need parental consent. Possibly, we state that individuals under 13 shouldn’t sign up on their own. In school context, COPPA allows school to consent on behalf of parents for educational tools.
  - We should not knowingly collect personal data from under 13 without consent. Likely, since most ACT takers are 15-18, this might not be an issue. But if younger (some start earlier), handle accordingly (maybe during signup, birth year selection – if under 13, instruct to have a parent or school create account).

- **PCI Compliance (Payments):**

  - Since we use a third-party for payments, much of PCI scope is on them. But we must implement per their requirements:
  - Our payment forms should tokenize card data directly to gateway (so our server never sees raw card number).
  - We’ll still need to protect any stored tokens and follow best practices. Possibly do periodic PCI SAQ if required by payment provider.
  - Do not store CVV or sensitive data. Maybe store minimal billing info if needed (and secure it).

- **Data Encryption:**

  - All traffic uses TLS 1.2/1.3. No HTTP for any login or personal data endpoints.
  - Encrypt sensitive data at rest in the database. At least things like passwords (hashed as said), and consider encrypting other PII fields in the DB (names, emails) especially if in a multi-tenant environment to mitigate broad exposure from an SQL injection or DB leak.
  - Ensure backups are encrypted.

- **Secure Development:**

  - Follow OWASP top 10: protect against XSS (sanitize any user-generated content like notes), SQL injection (use ORMs or parameterized queries), CSRF (for web forms, use anti-CSRF tokens on sensitive actions).
  - Regularly update libraries to patch vulnerabilities.
  - Possibly conduct periodic security audits or penetration tests, especially before going live in a big way.

- **Monitoring and Logging:**

  - Keep logs of logins (with IP/device), key actions like password change, etc. Use these to detect suspicious activities (multiple logins from different locations).
  - Monitor system for performance issues that could indicate DoS attacks and have rate limiting or IP blocking for such events.
  - If using cloud, use cloud security features (like AWS Cognito or Azure AD services if applicable, or at least their firewall and monitoring tools).

- **Data Retention Policy:**

  - Decide how long to retain user data. Likely, keep it as long as account is active. If account is inactive for X years, maybe alert them or purge? Not urgent but good to define:
  - For GDPR, don’t keep data indefinitely if not needed. Possibly anonymize or delete accounts that have been inactive for, say, 5 years (the user likely moved on from ACT by then).
  - But ensure before deletion, maybe attempt to contact or have in terms that we do this.

- **Third-Party Components:**

  - AI Tutor: If using external AI API, ensure we’re not inadvertently sending more data than needed. Possibly strip personal info from prompts. And ensure the provider will not store or use the query content beyond providing the result (OpenAI has policy where you can opt-out of data being used for training).
  - Video Hosting: If using YouTube or Vimeo, consider embed privacy options. Or if using our cloud, ensure the URLs are gated (maybe signed URLs that expire so random people can’t scrape video links).
  - Analytics trackers: If using something like Google Analytics on the web, be cautious about student data. Perhaps avoid or use minimal tracking with IP anonymization. For COPPA/FERPA, likely treat all student users as under privacy law, so don’t use invasive tracking or ad cookies.

- **Physical and Operational Security:**

  - Host on a secure cloud (AWS, etc.) with proper access control to servers (SSH keys, etc.).
  - Regular backups stored securely (and test restores).
  - Dev/QA environments should not have real user data, or if needed, sanitize it, to avoid leaks from there.

- **Transparency:**

  - Publish a clear Privacy Policy explaining what data we collect and how it’s used. E.g., state that data may be shared with school educators or with the AI processing service, etc.
  - Comply with any requirements to register data processing if needed (for GDPR, maybe have a Data Protection Officer if scale warrants).

- **User Controls and Safety:**

  - Allow users to manage privacy settings – e.g., if they want to hide their name on leaderboards if we had any (we didn’t specify leaderboards, but if we add, must allow opting out to not reveal identity).
  - Ensure any community feature (not really in scope now) is moderated to prevent harassment. Currently, no direct user-to-user communication, which avoids that risk.

- **Plan for Security Incidents:**

  - Maintain an incident response plan (who to contact, how to investigate logs).
  - Possibly have bug bounty or encourage responsible disclosure of any vulnerabilities found.

- **International Considerations:**

  - If expanding to EU, might need to designate an EU representative for GDPR, etc., and perhaps host EU data in EU data center to ease compliance (depending on strategy).
  - For now, likely mostly US, but keep code flexible.

By implementing the above, we aim to not only meet legal requirements but also build user trust. Students and parents will feel comfortable using the platform, and schools will be confident we’re a safe custodian of student data. Security and privacy are ongoing commitments, so these practices would be revisited and updated regularly.

**Key Security Measures Summary:**

- _Encryption:_ All student records encrypted in transit (HTTPS) and ideally at rest on servers.
- _Access Control:_ Strict role-based access and least privilege principle.
- _Monitoring:_ Logging and monitoring for unauthorized access attempts.
- _Annual training:_ (for internal team) on FERPA and privacy obligations, as recommended.
- _User Rights:_ Mechanisms to fulfill data access/correction/deletion requests in compliance with GDPR’s transparency and control requirements.
- _Policy:_ Adherence to published privacy policy terms and not using data for purposes beyond user’s expectation (e.g., don’t sell their data, don’t spam them outside the platform context).

Taken together, these ensure that the platform is a safe environment for students to learn, aligning with educational trust standards and legal mandates.

## Performance and Scalability Strategies

To provide a smooth experience for potentially thousands of users and to accommodate growth, the platform’s architecture must be scalable and performant. Here we outline performance requirements and strategies for scaling:

### Performance Requirements

- **Responsive UI:** Aim for page load times < 3 seconds on broadband for main student pages (dashboard, content). Interactions like submitting an answer or loading the next question should feel nearly instant (< 500ms).
- **Latency Targets:** Most API calls should respond within \~300ms under normal load, excluding external dependencies like AI processing which might take longer (AI responses we aim < 2-5 seconds). Keep 95th percentile response < 1s for typical non-AI requests.
- **Concurrent Users:** Design to handle at least _500 concurrent active users_ in the initial launch scenario (e.g., 500 students simultaneously taking tests or watching videos). The architecture should be able to scale to _thousands of concurrent users_ as adoption grows.
- **Throughput:** For example, if 1000 users are taking a test with 200 questions each, that could be 200,000 question submissions in a short period. The system should handle bursts of writes (answers saving) – maybe on the order of a few hundred writes per second sustained.
- **Auto-Grading:** Grading a test (comparing answers to key and computing score) should be efficient (O(n) with n questions, which is fine for n \~ 215). Even if many finish tests at the same time, that computation is trivial – ensure the database can handle result inserts concurrently.
- **Media Delivery:** Use Content Delivery Networks (CDNs) for static content (images, videos) to reduce load on core servers and speed up content delivery globally.
- **Resource Utilization:** Keep server CPU/memory usage within healthy ranges – e.g., < 70% utilization under expected peak, to allow headroom. Use load testing to verify and adjust capacity.
- **Uptime & Availability:** Aim for high availability – ideally 99.5% or above uptime. This means planning for minimal downtime deployments and redundancy to avoid single points of failure.
- **Capacity for Peak Events:** Perhaps around popular ACT test dates, usage might spike. We should scale up around those times (could be via auto-scaling triggers or manual schedule) to ensure no slowdowns when everyone practices last-minute.
- **Efficient Data Queries:** Analytics queries that aggregate lots of data should be optimized (maybe precomputed nightly or stored in a way that retrieval is fast). Ensure indices on database for common query patterns (like lookup by user ID, by class ID).
- **Gradual Degradation:** In extreme load, system should degrade gracefully (maybe queue some background tasks or temporarily disable non-critical features) rather than crash. For instance, if AI tutor API is overloaded, it might queue requests or tell users to retry, rather than affecting core practice functions.

### Scalability Strategies

- **Cloud Infrastructure:** Deploy on a cloud platform (AWS, Azure, GCP) to leverage easy scaling:

  - Use auto-scaling groups for stateless app servers – as load increases, automatically launch more instances.
  - Scale down during off-peak to save cost.
  - Use load balancers to distribute traffic evenly across servers.

- **Microservices (Modular Scalability):** Consider dividing the system into services that can scale independently:

  - e.g., separate services for the **Practice Engine**, **Content Service**, **AI Tutor Service**, **Notification Service**, etc. This way, if AI processing is heavy, we scale that service without impacting others.
  - The API Gateway will route requests to appropriate service.
  - Microservices can also isolate failures and simplify development, though add complexity, so might evolve into this as needed.

- **Database Scaling:**

  - Start with a robust relational DB (like PostgreSQL). As usage grows:

    - **Vertical scale** to a point (increase instance size, IOPS).
    - Then add **read replicas** to offload read-heavy operations like analytics queries or content queries, keeping primary for writes.
    - Potentially use **sharding** if data volume becomes huge – e.g., shard by user group (though likely not needed until extremely high user counts).

  - Use **caching** for frequent queries: e.g., cache the list of lessons or a user’s dashboard stats in memory (Redis or local cache) to avoid hitting DB every time.

- **Content Delivery Network (CDN):**

  - Serve static assets (CSS, JS, images) and especially videos via CDN nodes globally to reduce latency. E.g., host videos in cloud storage (S3) with CloudFront or Cloudflare CDN in front.
  - This takes load off our servers for media and speeds up content load for users in various regions.

- **Asynchronous Processing:**

  - Use background job queues for tasks that need not be real-time:

    - e.g., sending emails, generating PDF reports, heavy analytics crunching, or even AI tutor requests if we want to queue them.

  - This way, the web request returns quickly (just enqueue job) and a worker processes in background.
  - Use something like RabbitMQ or cloud queue service plus worker nodes.

- **Auto-Scaling AI Resources:**

  - The AI tutor usage might be spiky (lots of questions at once during homework time). If using an external API with pricing, maybe scale usage or have a pool of requests. If using an internal model, it may need separate GPU instances that scale up at peak usage.
  - Possibly set concurrency limits on AI requests to avoid overwhelming either our system or the external API – queue extras.

- **Parallelism and Threading:**

  - Ensure the web server can handle concurrent requests (e.g., use a multi-threaded or multi-process setup, typical in web servers or via cloud auto-scaling).
  - For tasks like grading multiple tests or generating reports, process in parallel if possible.

- **Statelessness:**

  - Design web app servers to be stateless (store session in a distributed cache or use tokens) so any server can handle any request. This enables easy horizontal scaling.

- **Localization for Global Scalability:**

  - If anticipating international usage, consider deploying in multiple regions (multi-region architecture) so that users in Asia hit an Asia-Pacific server, etc., for lower latency.
  - But then need to sync databases across regions (or separate by region if data can be siloed).
  - Initially, likely one region (e.g., North America) but cloud makes multi-region feasible when needed.

- **API Rate Limiting:**

  - To protect against abuse and ensure fairness, throttle heavy API usage which also helps performance for everyone.

- **Profiling and Load Testing:**

  - Conduct load tests (with tools like JMeter or k6) to simulate high user load, identify bottlenecks.
  - Profile code to find slow operations (like inefficient queries) and optimize them (add indexes, caching, or rewrite logic).

- **Algorithmic Efficiency:**

  - For large operations (like analytics over thousands of data points), ensure algorithms are efficient. For example, computing class averages should use set-based DB queries rather than fetching all results and summing in app memory.
  - If necessary, maintain running aggregates (update a running average each new score instead of recalculating all past scores each time).

- **Logging and Monitoring:**

  - Implement application performance monitoring (APM) to watch response times, DB query times, etc. Tools like New Relic or DataDog can help detect slow calls in production.
  - Monitor system metrics (CPU, memory, DB locks) so we can scale up before performance degrades drastically (trigger auto-scale or alarms).

- **Scaling the Notification System:**

  - Use cloud email/SMS services that handle scale (SES, Twilio). If sending bulk emails (like to all users), do it in batches or via provider’s bulk send features to avoid overwhelming our server.
  - Make notification sending asynchronous (queue them) so user actions aren’t slowed by waiting for email send.

- **Scalable Architecture Example:**

  - **Client** (Web, Mobile) -> **Load Balancer** -> **Web/API servers** (stateless, auto-scaled) -> **Database** (primary + replicas) and other services (cache, queue, AI service).
  - **CDN** in front of static content and perhaps a separate subdomain for videos content.
  - **Microservices**: possibly separate the AI tutor microservice behind an API (so if it needs special environment like GPU).

- **DevOps / CI-CD:**

  - Use containerization (Docker) so scaling out new instances is quick (maybe orchestrated with Kubernetes or simpler auto-scaling groups).
  - Ensure rolling deployments so we can deploy updates without downtime (load balancer shifts traffic gradually, using health checks).
  - Keep sessions unaffected during deploy by either sticky sessions or preferably stateless tokens.

- **Scaling Up vs Out:**

  - We prefer scaling out (horizontal) for web and workers to avoid single machine limits. For DB, scale up to a point, then read replicas (horizontal for reads) and eventually partition if needed.
  - For AI or special tasks, might scale vertically if needed (e.g., a bigger instance for AI).

- **Capacity Planning:**

  - Plan resource allocation based on user growth projections. E.g., if we plan to onboard a school of 1000 students next month, test the system with that load plus some margin.
  - Have a clear path for scale: know at what user count we might need to upgrade DB, etc., so it's proactive.

- **Backup and Recovery:**

  - Not exactly performance, but ensure backups (and a strategy for quickly restoring service if main DB fails). Possibly have a hot standby or use cloud managed DB with failover.
  - This ties to availability (scalability includes being resilient to failures).

- **Edge Caching:**

  - Consider edge caching for dynamic content where possible. For instance, maybe the content library changes rarely, so the API could allow caching of lesson list for some minutes at CDN edge.
  - Use ETag or Last-Modified headers so clients can cache responses and reduce load.

- **Batch Operations:**

  - If any heavy background jobs (like nightly re-computation of some analytics or generating personalized study plans for all users), schedule them in off-peak hours and optimize by doing in batches rather than all at once.

By implementing these strategies, the platform can **scale horizontally** to accommodate more users and higher load while maintaining performance. For example, if one day we have 100k users, we might have dozens of app servers behind load balancers, a cluster of database nodes or a move to distributed databases, and partitioned services – the architecture laid out here sets the foundation.

We will adopt a **“scale as you grow”** approach:

- Initially deploy a simple but scalable architecture (monolithic app, one DB) on cloud infrastructure that can scale up.
- As usage grows, split out services (e.g., move AI to its own service, add read replicas for DB) – this **modular scaling** ensures we handle bottlenecks individually.
- Use cloud auto-scaling and managed services to handle the heavy lifting of scaling infrastructure.
- Constantly monitor and load test to anticipate scaling needs, rather than reacting to fire.

This way, the platform can grow from serving a handful of pilot users to potentially tens of thousands of students across many schools or globally, without major rewrites – scaling will be a matter of allocating more resources and doing targeted optimizations as identified.

## UI/UX Expectations

A superior user experience is crucial for engagement, especially for a student-facing educational platform. While detailed visual design is outside the scope of this document, the following expectations and principles will guide the UI/UX design:

- **Clarity and Simplicity:** The interface should be intuitive for teenagers and busy educators alike. Navigation and workflows should require minimal explanation. Pages should avoid clutter, highlighting the primary actions (e.g., “Start Practice Test” should be a prominent button on the dashboard).
- **Consistency:** Use a consistent design language across all modules (colors, typography, button styles). For instance, if the “Take Test” button is green and rounded on the dashboard, the same style should be used for similar call-to-action buttons elsewhere.
- **Visual Hierarchy:** Employ headings, subheadings, and cards to break content into scannable sections. Important info (like the student’s current score or progress toward goal) should be larger or more prominently placed. Less critical details can be smaller or tucked in a secondary view.
- **Responsive Design:** The web interface should be fully responsive to work on various screen sizes (from laptop to tablet to smaller monitors). Elements should rearrange logically - for example, a sidebar might become a top menu on narrower screens.
- **Accessibility:** Design to WCAG AA standards:

  - Ensure sufficient color contrast for text (for readability by visually impaired or in bright light).
  - Provide text alternatives for icons/images (use alt tags, and avoid using color alone to convey meaning).
  - Make sure the interface is navigable by keyboard (for users who can’t use a mouse).
  - Support screen readers with proper semantic HTML structure.

- **Engaging Visuals:** Incorporate some visual elements to keep students motivated:

  - e.g., small icons or graphics for achievements, or subject-related imagery (like a math icon next to math content). But keep them lightweight and not overwhelming.
  - Perhaps use a progress circle or bar to visually represent progress toward goals, which can be motivating.

- **Feedback and Encouragement:** The UI should provide positive reinforcement:

  - After a test, show a congratulatory message, especially if improved (“Good job, you improved by 3 points!”).
  - Use encouraging language in AI tutor and notifications, as earlier described.

- **Error Prevention and Handling:**

  - Validate inputs (like registration fields) inline and show helpful error messages (not just “invalid input”, but e.g. “Password needs at least 8 characters”).
  - If a student tries to start a test with unsaved progress in another, confirm before discarding that progress.
  - Use modals or highlights to confirm destructive actions (like “Are you sure you want to reset this test?”).

- **Minimal Learning Curve:** Ideally, a student can log in and immediately understand where to go – e.g., a big “Start Practicing” on first login that guides them to either a diagnostic test or a tour of resources.
- **Onboarding Hints:** Provide a short onboarding for first-time users: maybe tooltips or a quick tutorial slideshow that introduces key areas (“This is your dashboard… here you can see progress. Click here to start a test. Check out the AI tutor for help anytime.”). Keep it brief and skippable.
- **Visual Design Alignment:** Perhaps use a modern flat design, with the platform’s branding colors (if ACT-related, maybe blues/greens to signify trust and growth). Use one accent color for action buttons to guide the eye.
- **Typography:** Use a clean, easy-to-read font. Possibly larger font sizes for content text to accommodate younger readers. Use headings and subheadings to structure content (e.g., in lessons, clearly differentiate sections).
- **White Space:** Don’t fear whitespace; a less cramped interface helps focus. Group related elements (like group by card or panel).
- **Mobile Considerations:** Already covered in mobile section, but ensure any web UI also works on tablet (some students may use iPads).
- **Internationalization Ready:** While initially English, design layouts that can handle longer text (if translated, some languages expand text length). Avoid hard-coding text into images. Use a system for string resources so that UI can be translated if needed in future.
- **Brand and Tone:** The tone of UI text should be friendly, supportive, and age-appropriate (teenagers but also formal enough for educators).

  - For example, avoid overly childish language, but also avoid overly academic/clinical tone.
  - Use second person (“You”) to speak directly to the user (“You have completed 3 of 5 modules”).

- **No Ads / Distractions:** The UI will not have third-party ads or unrelated banners, to maintain focus on learning (and to comply with likely ad-free educational environment).
- **Loading Indicators:** Use spinners or progress bars if a action takes more than a second, to reassure user that something is happening (e.g., “Grading your test...” spinner).
- **Session Continuity:** If a student leaves in the middle of something (closes browser), ensure when they return, the UI clearly shows their saved state (“Resume Test” if they had one in progress).
- **Profile & Personalization:**

  - Allow uploading a profile picture (not essential, but could personalize the portal, making it feel more personal).
  - Show their name in a welcome message (“Welcome back, Alex!”) to create a connection.

- **Search and Navigation:** If content library is large, a search bar and filters (subject, difficulty) should be easily accessible.
- **Help and Support UI:** Provide a link to help/FAQ or an intercom chat for support queries if needed. Possibly the AI tutor can answer some FAQ, but for technical issues, ensure a support contact.
- **UX for Teachers/Admin:** If teachers use the platform, their UI should be tailored:

  - e.g., a class selection drop-down if they manage multiple classes.
  - Summary dashboards focusing on class performance rather than personal.
  - Maintain similar look but with slightly different content emphasis.

- **Scenarios UX:**

  - _Taking a Test:_ UI should minimize extraneous elements (maybe a focused mode). Perhaps allow a “full-screen mode” on web to hide navigation during the timed test to mimic test environment.
  - _Reviewing Answers:_ Provide an easy next/previous navigation, perhaps a list of questions for jumping. Use color coding (green checkmark/red x) to mark correct/incorrect in review view.
  - _Progress Page:_ Use infographics (bar charts, line charts) to show progress, but also numeric values for clarity.

- **Gamification (subtle):** We can consider small gamified touches:

  - Badges or trophies for milestones (complete first test, streak of practice days, etc.). Display these in profile.
  - Leaderboard maybe not, as it can discourage some (and data privacy concerns comparing scores). If at all, maybe a user vs average line chart rather than naming others.

- **Content Presentation:**

  - For lessons: break text into short paragraphs with bullet points or numbered lists for steps, as per instruction guidelines (like we are writing here!). This reduces cognitive load.
  - Possibly incorporate interactive elements (like a mini-quiz question inside a lesson video as a pop-up question) if technology allows, but could be advanced.

- **Error States:**

  - If something goes wrong (server error), show a friendly message (“Oops, something went wrong. Try again or contact support.”) rather than a raw error. Possibly include a retry button.
  - If a page has no data (e.g., no tests taken yet), show an informative empty state: “No results yet – take a practice test to see your progress here.”

- **Future UI Scalability:**

  - Plan space for potential expansion (like if we add SAT prep or other exams, can the UI accommodate switching context? Perhaps in far future an exam toggle).
  - Or if adding more modules (like a forum or scheduling tool), ensure navigation can extend.

Essentially, the UX should make studying as _painless_ as possible: minimal friction to get to what they need (studying or analyzing progress), and even _enjoyable_ by providing encouragement and a sense of progress. A student should feel the app is a helpful coach, not a confusing system they dread using.

We will likely have professional UI/UX designers later craft the detailed designs based on these principles. Until then, any prototypes or wireframes will adhere to these expectations, ensuring that the end product is user-centered.

---

**Conclusion:** This document has detailed the comprehensive requirements for the ACT Exam Training SaaS platform, including functional modules, user stories, and critical considerations for performance, security, and user experience. It serves as a blueprint for development and implementation, aligning the team (product managers, developers, designers, stakeholders) on the vision and specifics of the platform. Following these requirements will help ensure we deliver a high-quality product that effectively helps students prepare for the ACT, while being scalable, secure, and delightful to use.
