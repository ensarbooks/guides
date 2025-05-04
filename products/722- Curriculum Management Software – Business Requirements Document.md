# Curriculum Management Software – Business Requirements Document

## Executive Summary

([21 Best Curriculum Management Software for 2025 | Research.com](https://research.com/software/best-curriculum-management-software)) _Figure: Teachers currently spend significant time on manual curriculum planning – averaging **5 hours** per week searching for resources and up to **9 hours** on developing curriculum ([21 Best Curriculum Management Software for 2025 | Research.com](https://research.com/software/best-curriculum-management-software#:~:text=The%20manual%20preparation%20of%20the,Learning%20Counsel%2C%202021)). This Curriculum Management Software (CMS) aims to drastically reduce that burden by digitizing and streamlining lesson planning, curriculum mapping, and collaboration._

This Business Requirements Document (BRD) outlines a comprehensive plan for an internal product team to develop a **Curriculum Management Software** solution. The software will empower educators and administrators to **plan, organize, and share curriculum** more effectively, aligning teaching content with standards and improving collaboration. Key features include intuitive **curriculum mapping** at lesson, unit, and year levels; customizable **lesson plan templates**; seamless **file and multimedia attachments**; robust **curriculum sharing** via a web portal; and **integrations** with Learning Management Systems (LMS), Student Information Systems (SIS), and electronic grade books.

The CMS will address critical challenges in education planning: ensuring that instructional materials are engaging and aligned to required learning standards, while saving time for teachers. High-quality curriculum alignment is crucial, as teachers face hundreds of standards per grade level ([21 Best Curriculum Management Software for 2025 | Research.com](https://research.com/software/best-curriculum-management-software#:~:text=To%20add%20to%20this%20workload%2C,Learning%20Counsel%2C%202021)) and consider alignment with state standards extremely important ([21 Best Curriculum Management Software for 2025 | Research.com](https://research.com/software/best-curriculum-management-software#:~:text=Curriculum%20management%20platforms%20facilitate%20the,software%20to%20properly%20manage%20documents)). At the same time, **81.5% of teachers** prioritize having engaging, compelling content in their curriculum ([21 Best Curriculum Management Software for 2025 | Research.com](https://research.com/software/best-curriculum-management-software)). By providing tools to map curriculum to standards and attach rich multimedia resources, this software will help meet both needs – fostering engaging content and rigorous alignment. Through automation and smart design, the platform will free teachers to focus more on instruction and students, rather than paperwork ([21 Best Curriculum Management Software for 2025 | Research.com](https://research.com/software/best-curriculum-management-software#:~:text=Effective%20teaching%20and%20learning%20is,the%20age%20of%20digital%20transformation)) ([21 Best Curriculum Management Software for 2025 | Research.com](https://research.com/software/best-curriculum-management-software#:~:text=Curriculum%20management%20software%20provides%20solutions,and%20selection%20of%20instructional%20materials)).

In summary, the vision is to deliver an all-in-one curriculum planning platform that improves **efficiency, collaboration, and instructional quality**. This BRD details the product vision, scope, stakeholders, use cases, requirements, design expectations, and implementation plan. It will serve as a blueprint for the development team to build a solution that supports continuous improvement in teaching and learning, ultimately contributing to better student outcomes through well-planned curricula.

## Product Vision and Scope

**Product Vision:** The Curriculum Management Software will be a **unified platform** for educators to design, organize, and refine curriculum plans across all levels – from individual lessons to full academic year curricula. The vision is to ensure every teacher can easily create **engaging, standards-aligned lessons** and see how they fit into the broader curriculum map, while collaborating with peers and administrators. By automating curriculum mapping and providing real-time collaboration tools, the system facilitates continuous improvement of teaching practices ([21 Best Curriculum Management Software for 2025 | Research.com](https://research.com/software/best-curriculum-management-software#:~:text=Curriculum%20management%20software%20provides%20solutions,and%20selection%20of%20instructional%20materials)). The ultimate goal is to enhance teaching effectiveness and student learning by making curriculum planning more **efficient, data-informed, and collaborative**.

**Scope:** The CMS will focus on core functionality that supports K-12 curriculum planning and internal collaboration within a school or district. Key in-scope features include:

- **Curriculum Mapping:** Tools to map curriculum structure vertically (across grade levels) and horizontally (across subjects) for a full academic year. This includes creating courses (by subject/class), units, and lessons, and visualizing how they connect. Alignment to academic standards and learning goals is in scope to ensure each plan meets required guidelines ([OpenCurriculum: Lesson planning, unit planning, and curriculum mapping and alignment software for K-12 schools tools](https://opencurriculum.org/#:~:text=Align%20your%20plans%20with%20standards,starting%20with%20the%20end%20first)).
- **Lesson and Unit Planning Templates:** A flexible template system for lesson plans and unit plans, allowing customizable sections (e.g. objectives, activities, materials, assessments) tailored to institutional or departmental needs. Templates can be standardized by administrators or personalized by teachers, supporting consistent yet adaptable planning formats ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=,Classroom%20to%20share%20with%20students)).
- **File Attachments and Resources:** Ability to upload or link **multimedia content** (documents, slide decks, images, videos, web links, etc.) directly to lesson and unit plans. All resources will be managed within the platform for easy retrieval, ensuring teachers have a one-stop repository for all materials related to a lesson ([Planbook - The Leader in Lesson Planning](https://planbook.com/#:~:text=,repository%2C%20or%20add%20your%20own)).
- **Curriculum Sharing and Collaboration:** A web-based portal where teachers can share their curriculum plans with colleagues and administrators. Fine-grained permissions (view or edit) will enable collaborative editing, peer review, and administrative oversight. Shared curriculum libraries and search functions will allow educators to discover and reuse materials across the institution ([OpenCurriculum: Lesson planning, unit planning, and curriculum mapping and alignment software for K-12 schools tools](https://opencurriculum.org/#:~:text=Share%2C%20find%2C%20and%20co,your%20colleagues)).
- **Integrations with LMS/SIS/Gradebook:** Technical integration points to connect the CMS with external systems. This includes single sign-on and class roster sync with the SIS, publishing lesson content or assignments to the LMS, and exchanging data with electronic grade books. These integrations ensure the CMS fits seamlessly into existing educational technology ecosystems ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=LTI%20Integration)) ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=OneRoster%20Ready)).

Out of scope for the initial version are features like **student performance tracking**, in-depth assessment analytics, or a built-in student gradebook (beyond connecting to existing gradebook systems). The CMS is **not** intended to replace an LMS for delivering content to students or a SIS for managing student records, but rather to complement them by focusing on curriculum design and planning. However, robust **APIs** will be considered to enable future expansion or third-party development in these areas.

The scope prioritizes internal use by teachers, curriculum designers, and school leaders within one organization (or district). Multi-school support (if needed for a district-wide rollout) will be considered in architecture but not fully built out in the first phase. By maintaining a clear scope centered on planning and collaboration, the project ensures a focused development effort on the features that deliver the most value to educators in the short term.

## Stakeholder Roles and Interests

Successful development and adoption of the CMS will depend on addressing the needs of several key stakeholder groups. The primary users – **teachers, curriculum designers, and school administrators** – each have distinct roles and requirements, which the system must accommodate. Below we identify each stakeholder type and their interests:

### Teachers (Lesson Planners and End Users)

Teachers are the daily users who will create and use lesson and unit plans in the system. Their needs include:

- **Efficient Lesson Planning:** Teachers want an intuitive interface to quickly create lesson plans, preferably using pre-defined templates so they don’t have to start from scratch each time. Reducing planning time is crucial, as teachers currently spend many hours on this weekly ([21 Best Curriculum Management Software for 2025 | Research.com](https://research.com/software/best-curriculum-management-software#:~:text=The%20manual%20preparation%20of%20the,Learning%20Counsel%2C%202021)).
- **Quality Content & Resources:** They need to incorporate a variety of engaging materials (presentations, worksheets, videos, links) into lessons. The system should make it easy to attach and organize these resources so that lessons are rich and ready for classroom use ([Planbook - The Leader in Lesson Planning](https://planbook.com/#:~:text=,repository%2C%20or%20add%20your%20own)).
- **Curriculum Alignment:** Teachers must ensure their lessons meet curriculum standards and learning objectives. They desire tools to map each lesson to required standards or skills, helping them guarantee coverage of the curriculum. This is very important to teachers – over 73% rate alignment with standards as _extremely important_ ([21 Best Curriculum Management Software for 2025 | Research.com](https://research.com/software/best-curriculum-management-software#:~:text=Curriculum%20management%20platforms%20facilitate%20the,software%20to%20properly%20manage%20documents)).
- **Collaboration & Sharing:** Teachers often collaborate in teams (grade-level teams or subject departments). They want to share their plans with colleagues, co-plan lessons, and view examples from peers. Features like commenting, co-editing, or version history would support reflective practice and mentoring.
- **Flexibility and Ownership:** While consistency is good, teachers also value flexibility to tailor plans to their classroom. They want the ability to customize templates or add personal notes and adjustments without breaking the overall structure. The system should empower teachers to “own” their plans while still aligning with school-wide templates.

### Curriculum Designers / Instructional Coordinators

Curriculum designers (or instructional coaches) are responsible for the **big-picture curriculum structure and quality** across classes and grades. Their interests include:

- **Curriculum Mapping Across Grades:** They need a macro view of the curriculum. The system should allow them to visualize how content progresses from one grade to the next, identify gaps or overlaps, and ensure a coherent sequence (vertical and horizontal alignment) across the school. For example, they should be able to see all units for a subject in one view and confirm that key topics are introduced and reinforced appropriately.
- **Standards Alignment and Consistency:** Designers will ensure that each course’s curriculum addresses the required standards and learning outcomes. They need reporting tools or dashboards to see which standards are covered where, and which might be missing, so they can advise teachers to adjust plans ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=,Powerful%20Insights)) ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=,with%20resources%20and%20instructional%20planning)). Consistency in how lesson and unit plans are documented is important – thus they will set up the templates and guidelines that teachers follow.
- **Resource Repository:** They often curate high-quality resources (texts, project ideas, assessments) for teachers to use. The CMS should provide a way to organize these shared resources (a “library” or repository) that can be attached to plans. Being able to update a resource in one place and have it available to many lessons is valuable.
- **Collaboration and Review:** Curriculum coordinators will use the system to review teacher plans, provide feedback, and approve or flag issues. They need permission to view/edit all curriculum content in their subject or grade purview. A workflow for **lesson approval** (where a teacher submits a lesson for review, and a coordinator marks it as approved or returns comments) would support quality control.
- **Data and Analytics:** Over time, designers will want to analyze curriculum data – e.g., how many lessons per standard, distribution of certain pedagogical strategies, etc. While advanced analytics might be a later feature, the system should at least capture data in a structured way to enable future analysis of the curriculum’s effectiveness (for instance, identifying redundancies or gaps ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=,with%20resources%20and%20instructional%20planning))).

### School Administrators (Principals and Academic Leaders)

Administrators need a high-level oversight of curriculum implementation and assurance that it meets organizational goals and compliance requirements. Their needs include:

- **Oversight and Accountability:** Administrators want to ensure that teachers are adhering to the curriculum and pacing guides. The CMS should allow them to easily review what is being taught in each class, each week, without sifting through paper plans. They might not edit plans directly, but they need viewing access and perhaps the ability to comment or require modifications.
- **Alignment with Standards and Policies:** School leaders are responsible for curriculum compliance with state or national standards and local policies. They will use the system’s reports to verify that all required standards are covered in lesson plans across the school ([21 Best Curriculum Management Software for 2025 | Research.com](https://research.com/software/best-curriculum-management-software#:~:text=Curriculum%20management%20platforms%20facilitate%20the,software%20to%20properly%20manage%20documents)). If the school has specific instructional frameworks (e.g., a required lesson structure or pedagogical model), the admin wants to see that reflected in every plan.
- **Ease of Use and Adoption:** Administrators will champion the tool’s adoption. They need the system to be easy for their staff to learn and use, otherwise it could become shelfware. Their interest is that the product provides real value (time saved, better collaboration) to justify any cost or training efforts. Success metrics like teacher usage rates and feedback will matter to them (addressed in Success Metrics section).
- **Security and Compliance:** Admins are concerned with student data privacy and overall system security. They want assurance that any integration (with SIS, etc.) is secure and that only authorized users (teachers, staff) can access the curriculum data. They will also be interested in backup plans (so years of curriculum work are not lost) and business continuity.
- **Stakeholder Communication:** In some cases, administrators might use the system to share parts of the curriculum with external stakeholders, such as school boards or parents (e.g. via a read-only portal or reports). While the primary sharing is internal, having an option to **export or publish** a curriculum overview to show parents “what will Grade 4 learn this year” could be valuable. This is a secondary use case, but part of the administrator’s interest in transparency.

### IT and Technical Staff (Secondary Stakeholder)

Although not primary users of the curriculum content, the school or district’s IT staff are stakeholders in terms of implementing and maintaining the system:

- **Integration and Data Management:** They will handle connecting the CMS with SIS, LMS, etc. They require that the software supports standard integration protocols (e.g., _Single Sign-On_, _OneRoster_ for class data, _LTI_ for LMS) to reduce custom work ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=LTI%20Integration)) ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=OneRoster%20Ready)).
- **Security and Hosting:** If self-hosted, IT will manage servers; if cloud, they will liaise with the vendor. They need the system to meet the organization’s security standards (encryption, user account management) and possibly compliance (FERPA, GDPR as applicable). They will also handle user provisioning, so features like bulk user upload or AD/LDAP integration matter.
- **Support and Maintenance:** IT will support teachers if there are technical issues. Thus, they care that the system is stable, has a good admin dashboard for troubleshooting, and that vendor support (if external) or documentation is available. Minimizing maintenance overhead (through automation, reliable updates, etc.) is in their interest.

By considering the perspectives of all these stakeholders – teachers, curriculum designers, administrators, and IT – the requirements in this BRD aim to ensure the system delivers value to each group and encourages broad adoption. Each feature and design decision will be weighed against how it improves the workflow for these users.

## Use Cases and User Stories

This section translates stakeholder needs into specific **use cases** and **user stories** that illustrate how the system will be used in practice. The use cases cover the core scenarios for planning, sharing, and managing curriculum. Each user story is formatted as **“As a [user], I want [goal] so that [reason].”** These narratives will guide feature development and ensure the product meets real-world usage requirements.

### 1. Curriculum Mapping and Course Planning

- **Use Case:** _Designing a Course Curriculum Map_ – A curriculum designer plans out an entire course for the year (e.g., 10th Grade Biology). They create a sequence of units, and for each unit specify the topics, duration, and key outcomes. The system helps visualize this structure in a timeline or outline.

  - **User Story:** _As a curriculum designer, I want to create a course outline with units and weeks, so that I can map out the content coverage for the year and ensure proper sequencing._
  - **User Story:** _As a teacher, I want to view the curriculum map for my subject, so that I understand the big picture and context for each unit I am teaching._
  - **User Story:** _As an administrator, I want to compare curriculum maps across subjects or classes, so that I can check for consistency and integration (e.g., cross-curricular themes)._

- **Use Case:** _Aligning Curriculum to Standards_ – While mapping the course, the user links each unit (or lesson) to relevant learning standards or competencies.
  - **User Story:** _As a teacher, I want to tag my units and lessons with state standard codes, so that I ensure all required standards are addressed and easily report on coverage._
  - **User Story:** _As a curriculum coordinator, I want to see a report of which standards are covered by each unit, so that I can identify any standards that might be under-represented in the curriculum._

_(During curriculum mapping, the system might offer analytics or suggestions – e.g., warning if a standard has no coverage, or showing overlaps. These advanced interactions can be part of future enhancements.)_

### 2. Lesson Planning with Templates

- **Use Case:** _Creating a Lesson Plan using a Template_ – A teacher develops a lesson plan for a specific day’s lesson, using the system’s template that includes fields like Objectives, Materials, Activities, Assessment, etc.

  - **User Story:** _As a teacher, I want to select a lesson plan template and be prompted to fill in key fields (like objectives, procedures, etc.), so that my lesson plans are well-structured and consistent with school requirements._
  - **User Story:** _As a teacher, I want to save a draft lesson plan and come back to edit it later, so that I can gradually refine my plan before teaching day._
  - **User Story:** _As an administrator, I want all teachers to follow a common lesson format, so that reviewing plans is easier and important elements (like learning objectives) are never missed._

- **Use Case:** _Customizing Templates_ – An administrator or lead teacher creates or modifies a template (for lessons or units) to fit new requirements (for example, adding a field for remote learning accommodations).
  - **User Story:** _As a curriculum designer, I want to customize the lesson plan template (add/remove fields or guidance text), so that it fits our instructional model and any new district mandates._
  - **User Story:** _As a teacher, I want the flexibility to have personal templates or add sections to my lesson (e.g., a section for “Reflective Notes”), so that I can tailor my plans to my teaching style while still including required elements._

### 3. Attaching Resources and Materials

- **Use Case:** _Adding Resources to a Lesson_ – A teacher attaches supporting materials to a lesson plan.

  - **User Story:** _As a teacher, I want to upload or link resources (PDFs, slides, videos, links) to my lesson plan, so that I have quick access to all teaching materials when I deliver the lesson ([Planbook - The Leader in Lesson Planning](https://planbook.com/#:~:text=,repository%2C%20or%20add%20your%20own))._
  - **User Story:** _As a teacher, I want to embed multimedia (images, audio clips) directly in my lesson instructions, so that I can present content directly from my lesson plan during class._
  - **User Story:** _As an administrator, I want resource files to be stored securely and organized by course/unit, so that we build a repository of vetted curriculum materials over time._

- **Use Case:** _Resource Library and Reuse_ – Teachers and designers search the repository for existing materials.
  - **User Story:** _As a teacher, I want to search for lesson materials or templates that other colleagues have shared, so that I can reuse proven resources instead of creating everything from scratch ([OpenCurriculum: Lesson planning, unit planning, and curriculum mapping and alignment software for K-12 schools tools](https://opencurriculum.org/#:~:text=Discover%20new%20ideas%20that%20help,your%20students%20learn%20faster)) ([OpenCurriculum: Lesson planning, unit planning, and curriculum mapping and alignment software for K-12 schools tools](https://opencurriculum.org/#:~:text=You%E2%80%99ll%20find%20hundreds%20of%20rigorous,students%2C%20into%20your%20own%20plans))._
  - **User Story:** _As a curriculum coordinator, I want to publish a set of common resources (e.g., a lab safety slideshow for all science teachers) in a central library, so that all teachers can easily find and attach it to their plans._

### 4. Sharing, Collaboration, and Review

- **Use Case:** _Sharing a Lesson or Unit with Peers_ – A teacher shares a completed lesson plan with their department or grade-level team for feedback or just as a resource.

  - **User Story:** _As a teacher, I want to share my lesson (or unit) with specific colleagues (or a group), so that they can view or edit it and we can collaborate on improving it ([OpenCurriculum: Lesson planning, unit planning, and curriculum mapping and alignment software for K-12 schools tools](https://opencurriculum.org/#:~:text=Share%2C%20find%2C%20and%20co,your%20colleagues))._
  - **User Story:** _As a teacher, I want to control permissions when I share (view-only vs. edit), so that I feel safe sharing drafts or get the right type of input._
  - **User Story:** _As a teacher, I want to browse or search lessons shared by others in my school, so that I can get new ideas and not duplicate work that’s already done._

- **Use Case:** _Administrative Review and Approval_ – A school has a policy that teachers submit weekly lesson plans to the principal or department head for approval.

  - **User Story:** _As a teacher, I want to submit my lesson plan for approval once it’s ready, so that my administrator knows it’s finalized and I receive credit for my planning._
  - **User Story:** _As an administrator, I want to review submitted lesson plans, leave comments or suggestions for improvement, and mark them as “Approved” or “Needs Revision,” so that I can guide instructional quality and ensure readiness._
  - **User Story:** _As an administrator, I want a dashboard of all teachers’ plan status (e.g., how many are submitted, approved, pending), so that I can quickly see compliance with planning expectations._

- **Use Case:** _Real-Time Co-editing and Comments_ – Two or more users edit or discuss a curriculum document within the system.
  - **User Story:** _As a teacher collaborating with a co-teacher, I want to concurrently edit the same unit plan and see each other’s changes, so that we can co-plan in real time rather than emailing files back and forth._
  - **User Story:** _As a curriculum coach, I want to comment directly on a teacher’s lesson plan (e.g., suggest a modification in the materials section), so that my feedback is contextual and the teacher can reply or adjust accordingly._
  - **User Story:** _As a teacher, I want to receive notifications when someone comments on or edits a shared plan of mine, so that I stay informed and can respond promptly._

### 5. Integration with External Systems

- **Use Case:** _Single Sign-On (SSO)_ – A teacher logs into the CMS using their existing school Google account (or Office 365, etc.).
  - **User Story:** _As a teacher, I want to log in to the curriculum system using the same credentials as my email (Google/O365), so that I have one less password to remember and access is seamless ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=Single))._
  - **User Story:** _As an IT admin, I want the system to support SSO (SAML, OAuth, etc.), so that account management is centralized and secure._
- **Use Case:** _Importing Class and Roster Data from SIS_ – The system syncs with the Student Information System to get the list of courses, class sections, and students.

  - **User Story:** _As a teacher, I want my class roster and schedule to automatically appear in the CMS (via SIS sync), so that I can organize my plans by class without manually entering class names or student lists._
  - **User Story:** _As an IT admin, I want the curriculum software to integrate via OneRoster or similar standard with our SIS, so that class data is up-to-date and we avoid double data entry ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=OneRoster%20Ready))._

- **Use Case:** _Publishing Lesson Content to LMS_ – After creating a lesson plan, a teacher pushes parts of it (like an assignment or resources) to the LMS for student access.

  - **User Story:** _As a teacher, I want to publish an assignment or resource from my lesson plan directly into Google Classroom (or Canvas, etc.), so that students can access the materials without me uploading it twice ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=,Atlas%20to%20your%20Google%20Classroom))._
  - **User Story:** _As a teacher, I want the option to export or print a student-facing version of the lesson (without my private notes) to share on the LMS or with students, so that I maintain one source of truth for content._
  - **User Story:** _As an LMS admin, I want the integration to respect LMS structures (courses, modules), so that content from the CMS appears in the right place for each class._

- **Use Case:** _Gradebook Sync_ – The teacher gives an assessment in a lesson and wants to record grades.
  - **User Story:** _As a teacher, if I include a graded activity in my lesson, I want to send its details (and possible student scores) to our gradebook system, so that I don’t have to re-enter grades manually._
  - **User Story:** _As a gradebook administrator, I want the curriculum system to only send allowed data (e.g., assignment name, due date, points) and not pull any sensitive student performance data back, to maintain security and FERPA compliance._
  - (Note: This use case might involve an LTI Advantage _Assignment and Grade Services_ integration or an API connection to the SIS/gradebook.)

### 6. Miscellaneous and Advanced Use Cases

- **Use Case:** _Printing and Reporting_ – A teacher or admin generates a report or printable view.

  - **User Story:** _As a teacher, I want to print my weekly lesson plans in a nice format, so that I can have a physical copy in class or turn it in if required._
  - **User Story:** _As an administrator, I want to export a curriculum map overview (units by month for each subject) to share in a board meeting, so that stakeholders see what is being taught each quarter._

- **Use Case:** _Search and Navigation_ – Searching across the curriculum database.

  - **User Story:** _As a teacher, I want to search for a keyword (e.g., “fractions”) and find all lessons, units, or resources that mention it, so that I can quickly find relevant plans or avoid duplication ([OpenCurriculum: Lesson planning, unit planning, and curriculum mapping and alignment software for K-12 schools tools](https://opencurriculum.org/#:~:text=with%20entire%20departments%20or%20PLCs,your%20school%20and%20beyond%20quickly))._
  - **User Story:** _As a new teacher onboarding, I want to browse last year’s curriculum plans for my grade, so I can learn from them and align my new plans accordingly._

- **Use Case:** _Archiving and Versioning_ – Year-end archive of plans and version control.
  - **User Story:** _As an administrator, I want to archive each year’s curriculum plans and start a fresh copy for the new year (while still referencing the old), so that we preserve history but have a clear workspace for updates._
  - **User Story:** _As a teacher, I want to see previous versions of a unit plan (or a change log), so that I can understand how it has evolved and possibly revert to an earlier version if needed._

These use cases and stories illustrate the broad usage scenarios for the CMS. They will inform the functional requirements in the next section, ensuring that each requirement ties back to a real user need. During development, the team can use these stories to create user acceptance criteria and test that the implemented features truly satisfy the intended goals.

## Functional Requirements

Functional requirements describe in detail **what the system should do** – the capabilities and behaviors it must exhibit to support the use cases above. We organize the functional requirements by feature area: Curriculum Mapping, Lesson/Unit Planning (Templates), Attachments, Sharing/Collaboration, Integrations, and additional general functionality. Each requirement is tagged (for reference) and described. These represent the **business needs** and will later be translated into technical specifications.

### 1. Curriculum Mapping and Course Organization

- **FR1. Course & Curriculum Structure:** The system shall allow creation of a hierarchical curriculum structure, including **Courses** (by subject, grade, or class) containing **Units**, which in turn contain **Lessons**. This three-level hierarchy (Course → Unit → Lesson) organizes content by time (e.g., year, semester, week) and topic. Users should be able to create, rename, reorder, or delete units and lessons within a course with a drag-and-drop or other easy interface. The structure should be visible in an outline or map view for quick navigation.
- **FR2. Visual Curriculum Map:** The system should provide a visual representation of the curriculum map for a course (e.g., a timeline or calendar view of units and lessons). Users can see the sequence of units over the term and click in to view details ([OpenCurriculum: Lesson planning, unit planning, and curriculum mapping and alignment software for K-12 schools tools](https://opencurriculum.org/#:~:text=Track%20your%20long,plans%20visually)). Optionally, a calendar integration can overlay the schedule (e.g., showing units/weeks on a calendar, possibly integrated with the school calendar for holidays).
- **FR3. Scope & Sequence Overview:** For administrators and designers, the system shall offer a “scope and sequence” report or view that displays the coverage of topics or standards across units and across grade levels. For example, the software can generate a matrix or sequence document that lists units for each grade side by side to facilitate vertical alignment checks ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=,and%20Sequence)) ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=,your%20curriculum%20and%20make%20adjustments)).
- **FR4. Standards Alignment:** Users (teachers or designers) shall be able to **align units and lessons to learning standards or objectives**. This involves selecting one or multiple standards from a standards database (state standards, Common Core, etc.) and tagging them to the lesson/unit ([OpenCurriculum: Lesson planning, unit planning, and curriculum mapping and alignment software for K-12 schools tools](https://opencurriculum.org/#:~:text=Align%20your%20plans%20with%20standards,starting%20with%20the%20end%20first)). The system should provide an easy lookup (e.g., search by code or keyword) for standards. An initial repository of standards can be provided (covering common state and national standards), and the ability to import custom standards is also required ([OpenCurriculum: Lesson planning, unit planning, and curriculum mapping and alignment software for K-12 schools tools](https://opencurriculum.org/#:~:text=match%20at%20L122%20national%20or,in%20mind%2C%20in%20a%20breeze)). This alignment data should be reportable (e.g., a report of all standards covered in a course).
- **FR5. Mapping Prerequisites and Skills (Optional/Future):** (Not necessarily for MVP) The system may allow mapping relationships between units or lessons (e.g., marking that “Unit 5 builds on Unit 3” or “Lesson A is prerequisite to Lesson B”) and visualizing learning pathways. This can help in understanding dependencies. This is a stretch goal that could evolve into more advanced curriculum analytics.

### 2. Lesson and Unit Plan Templates

- **FR6. Template Library:** The system shall support **lesson plan templates** and **unit plan templates**. An authorized user (e.g., admin or curriculum designer) can create a template that defines a set of fields/sections for a lesson or unit plan. Examples of fields: _Lesson Title, Grade Level, Duration/Date, Objectives, Standards, Materials, Activities/Procedures, Assessment, Reflections_. Templates can include rich text instructions or example text to guide teachers on what to fill in each section.
- **FR7. Customizable Fields:** It shall be possible to customize the number and type of sections in a template. For instance, up to a certain number (e.g., 10) sections can be defined ([Planbook - The Leader in Lesson Planning](https://planbook.com/#:~:text=Image%3A%20Planbook%20Lesson%20Editor)), with each section being a rich-text field, a dropdown (for predefined values), a checklist (e.g., “21st Century Skills addressed”), or other field types as needed. This flexibility allows different subjects or schools to tweak the plan format.
- **FR8. Multiple Templates & Selection:** The system should allow multiple templates to exist (for different purposes). For example, an elementary school might have a different lesson format than a high school, or there might be a special template for labs vs. regular lessons. When creating a new lesson or unit, a teacher can choose from available templates or the default template assigned to that course ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=,Classroom%20to%20share%20with%20students)).
- **FR9. Template Enforcement:** Administrators can assign a default template to be used for all lessons in a certain course or grade, ensuring consistency. Alternatively, the system can allow teachers to pick but warn if they diverge from the standard. The template should enforce required fields (e.g., cannot mark a lesson complete until certain fields like Objectives are filled out).
- **FR10. Lesson Plan Editor:** The system shall provide a user-friendly **editor** for inputting lesson plan details according to the chosen template. This includes a rich-text editor for narrative fields (supporting basic formatting, bullets, tables, equations for STEM subjects, etc.), and attachments for each section if needed (e.g., attach a file specifically to the “Materials” section). The editor should allow saving as draft and autosave frequently to prevent data loss.
- **FR11. Unit Plan Support:** Similarly, a Unit plan (which could span multiple lessons) will have its own template and editor. Typical unit plan fields might include _Unit Overview, Essential Questions, Skills Developed, Summative Assessment, etc._ The unit plan can serve as a cover page for the collection of lessons. Lessons within a unit might inherit some info from the unit (e.g., overarching objectives).
- **FR12. Reusable Template Components:** (Optional) The system could allow template sections or components to be reused or repeated. For instance, a template might include a repeatable section for “Activities” if a lesson has multiple distinct activities. This is a nice-to-have to increase flexibility of templates.

### 3. File Attachments and Content Management

- **FR13. Attach Files to Plans:** Users shall be able to attach files to a lesson or unit. This includes uploading files from their computer or attaching from integrated cloud storage (Google Drive, OneDrive, etc. if integrated). Multiple files can be attached to one lesson. Common file types like PDFs, Word/Google docs, PPT, images, audio/video files should be supported. The system should store these files securely and associate them with the lesson/unit.
- **FR14. Attach Links and Media:** In addition to files, the system should allow attaching **URLs** (links to external websites or online resources) and embedding media. For example, a YouTube video link could display a playable thumbnail, or an image could be embedded directly in the lesson content. This makes lesson plans more interactive and saves teachers time in finding the link during class.
- **FR15. Attachment Library/Repository:** All uploaded attachments should be managed in a repository. Each file might be linked to one or multiple lessons. Users should have a view where they can see all their uploaded files, possibly organized by course or tags. This allows reusing a file in another lesson without uploading again. An advanced feature could be global library (maintained by admins) vs personal library for each teacher.
- **FR16. Version Control of Attachments:** If a user updates a file (e.g., reuploads a newer version of a worksheet), the system could maintain versions or at least warn that an update will affect all lessons where that file is used. This ensures consistency (especially if a resource is shared widely).
- **FR17. Capacity and File Size:** The system should support a reasonable file size limit (e.g., up to 100MB per file, configurable) and a quota per user or course (depending on storage capacity planning). These limits can be set by the admin to manage storage usage. If the system integrates with external storage (like Google Drive), files might not count against the system’s storage.
- **FR18. Search within Attachments:** (Optional/Advanced) For certain file types (like PDFs or docs), having a search index could allow users to search the content of attachments. This could be useful to find where a particular document is used or to search text within curriculum documents. This is a more advanced requirement that can be in a later phase if feasible.

### 4. Curriculum Sharing and Collaboration Features

- **FR19. Share with Individuals or Groups:** Users shall be able to share any curriculum element (lesson, unit, or entire course) with other users in the system. Sharing can be to specific individuals (by name) or to predefined groups (e.g., all Biology teachers, or a PLC group). The system should leverage existing user accounts and group definitions for ease. Permissions include **View Only** or **Edit** access. For example, a teacher can allow a colleague to co-edit a lesson, or allow the department head to just view it ([OpenCurriculum: Lesson planning, unit planning, and curriculum mapping and alignment software for K-12 schools tools](https://opencurriculum.org/#:~:text=Share%2C%20find%2C%20and%20co,your%20colleagues)).
- **FR20. Permission Inheritance:** If a user shares a unit, by default all lessons under that unit become visible to the share recipients as well (inheritance of permissions), unless overridden. Similarly, sharing a whole course curriculum would share all units/lessons within. This “trickle down” of permissions ensures that sharing at a higher level automatically covers the contents ([OpenCurriculum: Lesson planning, unit planning, and curriculum mapping and alignment software for K-12 schools tools](https://opencurriculum.org/#:~:text=Share%2C%20find%2C%20and%20co,your%20colleagues)).
- **FR21. Shared Curriculum Library:** The system will provide a **Curriculum Library** area where users can browse content that has been shared with them or with groups they belong to. For example, an English teacher can go to a shared library and see all unit plans shared by the English department. The library should have filters by subject, grade, teacher, etc., and a search function ([OpenCurriculum: Lesson planning, unit planning, and curriculum mapping and alignment software for K-12 schools tools](https://opencurriculum.org/#:~:text=with%20entire%20departments%20or%20PLCs,your%20school%20and%20beyond%20quickly)).
- **FR22. Collaboration Editing:** When multiple users have edit access to a plan, the system should support collaborative editing. This could be implemented as real-time co-editing (like Google Docs style where two users can type concurrently) or a simpler approach like lock/edit (only one editor at a time with locking). Real-time editing is preferred for a modern collaborative experience, but it’s complex; at minimum the system should prevent conflicting edits (e.g., by locking a lesson when someone is editing, or merging changes intelligently).
- **FR23. Commenting and Annotations:** Users with access to a plan (view or edit) should be able to leave comments or feedback. This can be a general comment thread on the lesson/unit as a whole, and/or specific annotations on a section of the plan (e.g., comment on the “Assessment” section to suggest a change). The system should notify the owner (and possibly other collaborators) when new comments are made. There should be a way to resolve or reply to comments, supporting an iterative feedback process ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=,Discussions)) ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=,a%20unit%2C%20or%20a%20report)).
- **FR24. Notifications:** The system shall provide notifications for collaboration activities – e.g., when a plan is shared with you, when someone comments on your plan, when an edit is made by a collaborator, or when an admin approves/returns your submitted plan. Notifications could be in-app (a notification bell icon) and optionally email alerts depending on user preferences.
- **FR25. Approval Workflow (Optional Config):** For schools that require administrative approval of plans, the system should allow an **approval workflow** to be configured. This means a teacher can mark a lesson or unit as “Ready for review” (or change its status to submit), an admin user can then mark it as “Approved” or “Needs changes” with comments. Status tags like Draft/Ready/Approved/Taught could be used (as shown by colored labels in some systems) to track the stage of each lesson. This feature should be optional per institution or per course, since not all will use formal approvals.
- **FR26. Revision History:** The system should maintain a **history of changes** for each lesson and unit (at least for key fields). This allows users to see what changes were made, and by whom, in collaborative scenarios. It could be a simple version log or full version restore capability. For initial release, even tracking last edited timestamp and user might suffice, with deeper version history as a later enhancement.

### 5. Integration Functional Requirements

_(Detailed technical requirements for integration are in a later section; here we outline the functional behavior visible to users related to integration.)_

- **FR27. Single Sign-On Access:** Users shall log in via Single Sign-On using institutional credentials (e.g., Google Workspace for Education account, Microsoft Office 365 account, or SAML/ADFS). The system will integrate with these identity providers so that users do not need a separate username/password. From a user perspective, login might redirect to Google/Microsoft and then back to the CMS, establishing a session ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=Single)).
- **FR28. Class Data Sync:** The system shall import basic class information from the SIS or scheduling system. This includes the list of courses/classes a teacher teaches, student rosters (if needed for any reason, though primarily the focus is on teacher planning, having student names might not be critical unless sharing with students or taking attendance within the plan, etc.). At minimum, knowing the teacher’s courses and class sections (and their timetable) will personalize the experience (e.g., show “Grade 9 Algebra – Section 2” as a planning context). This sync might be one-time at semester start and whenever changes occur (via an API or file import).
- **FR29. LMS Publishing:** The system shall allow a teacher to push or export content to an LMS. At simplest, this could be: **Export lesson as PDF** to upload, but we aim for tighter integration: for supported LMS (like Canvas, Schoology, Google Classroom), the teacher can click “Publish to LMS” for a lesson or assignment within it. For example, in Google Classroom integration, a teacher could choose a lesson’s attached assignment and create a Classroom assignment for students in one step ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=,Atlas%20to%20your%20Google%20Classroom)). In Canvas, an LTI link might allow the lesson plan to be viewed by students (with certain sections hidden). The exact functionality might vary by LMS, but the requirement is to avoid double entry of content.
- **FR30. Gradebook Integration:** If the teacher uses the CMS to plan an assessment, they should be able to send the assessment outline to the gradebook or LMS gradebook. For instance, via the LMS’s gradebook or via SIS if that is the gradebook, an entry for that assignment could be created. Full two-way grade sync (like pulling student scores back) is not a core requirement for the planning tool (since grading is typically done in LMS/SIS), but we should at least consider one-way push of assignment info. Alternatively, the system could integrate with a tool like Google Classroom’s grades or just ensure that if content is pushed to LMS, any grading is done there.
- **FR31. Calendar Integration:** The system could integrate with teachers’ calendars. For example, a teacher might want their lesson schedule to appear on their Google Calendar (with maybe the lesson title on each date). So an integration or export to Google Calendar or Outlook could be offered. This helps teachers schedule and also helps with reflection when looking back at what was taught each day. It might also tie in with LMS which often have calendars for due dates.
- **FR32. API Availability:** The system shall expose an **API** for key data (lessons, units, courses, standards alignment, etc.) so that it can integrate with other systems not explicitly planned (or allow custom reports). For instance, a district might want to pull curriculum data into a data warehouse. Having a secure REST API or data export function (CSV, etc.) for courses and their plans is a requirement for openness. This also future-proofs the system for unforeseen integration needs.
- **FR33. Data Import/Export:** In addition to direct integrations, allow import/export of data in standard formats. E.g., importing a curriculum from a CSV or exporting a unit to PDF/Word for printing. Particularly, an export of the entire course curriculum (all units and lessons) in a human-readable format (PDF or doc) might be needed for accreditation reviews or backups.

### 6. Additional General Requirements

- **FR34. User Management & Roles:** The system shall have a user management module where admin users can create accounts (if not using SSO provisioning), assign roles (teacher, admin, designer, etc.), and organize users into groups (departments, grade-level teams) for sharing purposes. Roles determine access rights (e.g., only Admin role can create templates or approve lessons).
- **FR35. Dashboard/Home Screen:** Upon login, each user should see a dashboard. For teachers, this might list their courses/classes and upcoming lessons (perhaps a calendar of the current week’s lessons to plan). For admins, the dashboard might show an overview like how many lessons are ready or a summary of recent activity. This helps users navigate to their tasks quickly.
- **FR36. Search and Filter:** A robust search function is required, to search across lesson titles, content, attachments names, standards, etc. Filters should allow narrowing results by grade, subject, teacher name, date, etc. This search powers finding existing curriculum content quickly (which is critical given the volume of plans teachers produce).
- **FR37. Performance and Scalability (usage perspective):** The system must handle the typical usage patterns of a school. For example, multiple teachers may be editing at the same time (especially Sunday nights or common planning times). It should load curriculum views quickly (a teacher shouldn’t wait long to open their lesson). We anticipate usage where each teacher may create on the order of 180 lesson entries per year (one per teaching day) – the system should handle that data size and even years of accumulation without slow-down.
- **FR38. Help and Guidance:** There should be contextual help for users – e.g., an onboarding tour for new teachers, tooltips or example text in templates to guide what to write (particularly helpful for new teachers learning how to do lesson planning). This requirement ensures the product is not just a repository but also aids in building teacher capacity.

Each functional requirement above is considered “fulfilled” when the implemented system demonstrates the described behavior under real-world conditions. The development team will trace these requirements into design and test cases. Prioritization can be applied – for example, core planning and sharing features (FR1–FR3, FR6–FR10, FR13–FR15, FR19–FR21) are likely **Must-haves** for the Minimum Viable Product (MVP), whereas some advanced features (FR5, FR18, FR25, FR31, etc.) might be scheduled for later phases.

## Non-Functional Requirements

Non-functional requirements specify overall qualities and constraints of the system – how it should perform, how reliable it is, security standards, usability, etc. Even though these don’t map to specific user stories, they are critical to the system’s success in a production environment and for user acceptance.

**1. Performance and Scalability:** The application should be responsive and perform well with many users and data:

- Typical page loads (e.g., opening a lesson plan or loading the curriculum map) should occur in under 3 seconds for a standard broadband user.
- The system should support at least **N** concurrent users (where N is the number of teachers in the district, plus some margin for peak usage) without performance degradation. For example, if 100 teachers all log in on Monday 7am to check their plans, the system handles it smoothly.
- It should scale to manage multiple years of curriculum data. As years go by, archived plans might accumulate; the system should either archive older data to keep current operations fast, or be optimized to handle a large dataset (e.g., 5+ years of plans for all teachers).
- Attachments storage and download should be optimized via CDN or caching such that large file downloads don’t slow down the whole system.

**2. Reliability and Availability:** The CMS should be a reliable tool that educators can depend on daily:

- Target uptime should be at least **99%** during the school year for critical functionalities. Any maintenance or downtime should be scheduled during off-hours (e.g., late night or weekends) and communicated in advance.
- The system should have backup and recovery procedures. For example, database backups at least daily, and the ability to restore with minimal data loss (maybe at most one day’s work lost in worst case).
- If a failure occurs (server crash, etc.), the system should recover gracefully, and in-progress data (like an open lesson being edited) should not be lost thanks to autosave features.
- Versioning and audit logs (for internal recovery of mistakenly deleted items) should be available to admins. For example, if a teacher accidentally deletes a unit with lessons, an admin can restore it from a recycle bin or backup within a reasonable time frame.

**3. Security:** Since the system contains potentially sensitive information (especially if any student data is integrated, or even teacher’s intellectual property in lesson materials):

- It must enforce secure authentication (SSO or strong passwords if local accounts are used). Passwords, if any, stored must be hashed and salted.
- All data in transit should be encrypted via HTTPS. If self-hosted, the institution will install an SSL certificate; if cloud, the service must provide HTTPS endpoints.
- Data at rest should be encrypted on the server (especially any sensitive fields, though curriculum data is not highly sensitive, but integration credentials or user personal info is).
- Role-Based Access Control: Users can only access data they are permitted to. A teacher should not see another teacher’s plans unless shared. Admins can see more but only within their school’s context (if multi-tenant, no cross-school leakage). The system should validate permissions on every request (e.g., you cannot fetch a lesson by ID via URL if you don’t have rights).
- Regular security testing (penetration testing, code vulnerability scans) should be conducted, especially if the product will be widely used or hosted online. This ensures protection against common web threats (OWASP top 10, etc.).
- **Compliance:** If student data (even just names in rosters) is stored, the system must comply with **FERPA** (in the U.S.) meaning access to student-identifiable data is restricted to authorized school officials, and data is used only for educational purposes. Also, if the product is used in the EU or other regions, GDPR and other privacy laws apply for personal data (like teacher accounts info, etc.). This means clear data retention policies, ability to delete personal data if requested, etc.
- The software should log user activities (especially admin-level changes, or who shared what with whom) for auditing. This helps trace any misuse.

**4. Usability and Accessibility:**

- The application should have an intuitive UI that requires minimal training. Teachers and staff should be able to perform key tasks (creating a lesson, sharing it) with few clicks. We assume a varied range of tech proficiency among teachers, so design must be user-centric and tested with actual users for feedback.
- **Accessibility:** The UI must adhere to accessibility standards (WCAG 2.1 AA or equivalent). This includes providing text alternatives for icons, keyboard navigability (important for those who might not use a mouse), sufficient color contrast, and screen-reader compatibility for visually impaired users. While most users are teachers (who presumably don’t have severe impairments affecting computer use), public schools often have staff with varying abilities, so it’s important. Also, if at any point content is shared with students or parents via the system, accessibility becomes even more critical.
- **Browser Compatibility:** The web application should support the latest versions of major browsers (Chrome, Firefox, Edge, Safari) and likely the browsers that school devices use (some schools use iPads – Safari, or Chromebooks – Chrome). It should degrade gracefully on older browsers or at least warn the user if something might not work.
- **Responsive Design:** The interface should be responsive to different screen sizes. Teachers might use it on their laptops primarily, but some might open lesson plans on a tablet or phone. At least a view-only or minor editing capability on mobile would be useful (e.g., a teacher checking the lesson on their phone in class, or uploading a photo of board work as an attachment on the fly). Ideally, core functions work on a tablet, and basic viewing works on a phone.

**5. Maintainability and Extensibility:**

- The system should be built with a modular architecture that allows future enhancements (e.g., adding new modules like analytics). Clear separation of concerns (front-end, back-end, integration interfaces) is expected so that updates to one area don’t break others.
- It should have a configuration setup for different schools’ needs (like enabling/disabling the approval workflow, customizing templates, etc.) without requiring code changes – i.e., a lot of these should be data-driven or configurable through an admin panel. This makes the product usable by multiple institutions with varying processes.
- Documentation and code quality are internal requirements – the internal team should maintain good documentation for the code and user-facing documentation for the product, to simplify onboarding new developers and supporting the product long-term.

**6. Support and Training:** (If relevant to mention in BRD)

- The vendor or product team should provide training materials (tutorial videos, help center articles) for end-users. While not a software requirement per se, including this ensures that upon rollout, users have the resources to learn the system effectively.
- There should be an easy way for users to get support or give feedback – maybe a “Help” link or a way to submit feedback from within the app, which routes to the support team or product team’s ticket system.

These non-functional requirements ensure the system not only has the features needed but also delivers them in a reliable, secure, and user-friendly manner. They will guide decisions in architecture, technology choice, and testing (e.g., performance testing, security audits, usability testing sessions) throughout the project.

## UI/UX Expectations and Wireframe Concepts

The user interface and user experience design of the CMS are critical for adoption. Teachers and administrators are busy professionals; they will only embrace the system if it is intuitive, efficient, and pleasant to use. This section outlines the UI/UX principles, key screen mock-ups, and interaction design ideas to guide development. The design should follow a clean, modern web application style, consistent with common tools teachers use (like Google Classroom, etc.), so that it feels familiar.

**Overall Design Principles:**

- **Clarity and Simplicity:** Each screen should have a clear primary purpose. For example, a “Lesson Editor” screen focuses on editing content, while a “Curriculum Map” screen focuses on navigation of units. Avoid overwhelming users with too much information at once; use progressive disclosure (details when needed).
- **Consistency:** Use a consistent layout for lesson plans and unit plans. If every lesson has sections in a certain order, the UI should present them in that order. Buttons and icons (save, edit, share) should be uniform across the application.
- **Navigation:** Provide easy navigation between related entities. For instance, from within a lesson plan, the user should see which unit it belongs to and have a one-click access back to the unit or course view. A sidebar or breadcrumb navigation can help orient where you are (Course > Unit > Lesson).
- **Responsiveness:** Ensure the layout adapts to different screen sizes. On a large screen, maybe a two-column layout can show lesson content and a list of lessons. On a small screen, those collapse into single column.
- **Visual Appeal:** Use school-friendly, professional aesthetics – possibly the ability to apply a school’s branding (logo, colors) if this is a multi-tenant product. Include icons or visual cues for important actions (like an icon for attachments, a special marker for standard alignments etc.). However, keep it clean and not overly cluttered.

([Planbook - The Leader in Lesson Planning](https://planbook.com/)) _Figure: Example of a lesson plan editor interface in a curriculum planning tool. This interface (from a teacher’s perspective) provides structured sections such as Standards, Strategies, Lesson content, Homework, Resources, and Attachments. Key details like lesson title, date/duration, and unit/theme are highlighted at the top. Status labels (“Approved”, “Ready”, “Taught”) allow tracking the lesson’s stage. The rich text editor in the Lesson section lets teachers input detailed plans (e.g., Whole Class vs Small Group instruction) with formatting tools. Tabs or sections for Standards and Resources indicate that teachers can directly align the lesson to standards and attach relevant materials. This UI demonstrates a clean separation of different aspects of the lesson plan, making it easy for teachers to fill out and for reviewers to find specific information._

**Key Screen Wireframes:**

1. **Dashboard/Home:** Upon login, teachers see a dashboard listing their courses or classes. For each course, it might show the current unit and upcoming lessons. There could be a calendar view of the week’s lessons across all their classes. Administrators might see an overview of all courses or a summary like “X out of Y teachers have updated their plans this week”. A quick action button for “Create Lesson” or “Plan Unit” could be prominent.

2. **Curriculum Map View (Course View):** This screen shows the structure of a single course (e.g., “Biology 10”). It might list Units in order (perhaps as collapsible sections, or cards on a timeline). Each Unit shows its title, timeframe (e.g., Sept 1–Sept 30), and maybe the main standards or objectives. Inside each unit, the lessons are listed by date or sequence. The teacher can click on a unit to edit its details (opening a Unit edit dialog or page). They can also drag lessons to reorder (if sequence matters outside of dates) or adjust scheduling. An alternative is a **calendar view** where each week is a column and units/lessons are blocks within the calendar (useful for seeing pacing). The UI should allow toggling between list/outline view and calendar view for flexibility.

3. **Lesson Plan Editor:** As shown conceptually in the figure above, the Lesson Plan editor page will have fields as per the template. Likely it will scroll vertically through sections: Title, Date/Duration, Standards (with a “Choose Standards” button to pop up a selection dialog), then sections like Objectives, Activities, etc. Each section might be a rich text field. Attachments could be managed via an “Attachments” panel or a sidebar where teachers can drag and drop files or click “Add Attachment”. If templates have tabs (like the example shows tabs for Standards, Strategies, Lesson, Homework, etc.), the UI might implement these as tabbed panels or simply as header separators on one page. Save/Publish actions should be clearly accessible (maybe a “Save” button that becomes “Saved” auto if autosave, and a “Submit for Review” if an approval workflow is on). Also an indicator of last edit time is useful (e.g., “Last edited 5 minutes ago by Alice”).

4. **Unit Plan Editor:** Similar to Lesson Editor but fields differ. Could be a simpler form (since a unit plan might be one page of text fields). It might include a field to list which lessons (or how many lessons, or lesson titles) are in that unit, either automatically generated or manually listed. Possibly a field for “Culminating Project” or “Assessment” at unit level. The Unit editor UI should integrate with the course view – e.g., maybe it’s a side panel that opens when you click a unit in the map.

5. **Sharing & Collaboration UI:** When a teacher wants to share, there should be a **Share button** on relevant pages (lesson, unit, or course). Clicking it opens a dialog to add collaborators – like entering names or choosing a group, and setting view/edit rights. A teacher should also see who currently has access (a list of collaborators). For collaboration, if multiple users are editing, maybe an icon or note “John Doe is also editing this lesson” could show (if real-time collab is implemented). Comments could appear in a sidebar or as annotations (like little comment icons next to sections). A centralized **Notifications panel** will show things like “Principal commented on Lesson XYZ” or “Your Unit 2 was approved”.

6. **Admin Template Design UI:** For admins to create templates, a UI likely in the admin settings area would allow adding template sections. This might look like a form builder: enter section title, choose field type (text, rich text, dropdown), optional guidelines, etc., and order them. The result is saved as a template which teachers can then use. The admin should also be able to set which template applies to which course or teacher group.

7. **Integrations UI:** Not heavily used by teachers except maybe initial linking. For example, an integration settings page where a teacher can link their Google Drive or Google Classroom account (if not automatically via SSO). Or a setting to enable calendar sync. Many integrations will be behind-the-scenes or configured by IT/admin (like SIS sync is not a UI thing for teachers). But a teacher might see an option like “Push to Google Classroom” on a lesson if that integration is active.

8. **Reports/Analytics (Future):** Possibly an admin view where they can run reports, like “Standards Coverage Report” which shows a table of standards vs units. Or a usage report showing how many plans each teacher has done. This could be either an export or an on-screen chart. This is lower priority for initial UI design, but something to keep in mind for extensibility (maybe include a placeholder in UI navigation for “Reports”).

**UI/UX for Ease of Use:** The design should minimize clicks for common tasks. For instance, to create a week’s worth of lessons, maybe the teacher can copy a previous week as a starting point or use a template clone. We might incorporate features like _“duplicate lesson”_, _“bump lesson to next day”_ if a schedule changes (common in planning tools to adjust when something gets delayed). Also, keyboard shortcuts for power users (like Ctrl+S to save, etc.) could be considered.

**Accessibility and Testing:** The UI designs must be tested with actual users (teachers) to gather feedback. The product team should conduct usability testing on wireframes and prototypes to ensure that the navigation and layout make sense to educators. The design should avoid assumptions that users will read lengthy manuals – instead, incorporate visual cues and small help texts where needed.

By focusing on a streamlined UX, the CMS will become a helpful daily tool rather than a chore. The wireframe concepts here will be elaborated into high-fidelity designs by the UX team, but the development team should keep these principles in mind to implement the frontend accordingly.

## Workflow Diagrams and Data Models

To better understand the system’s operation and structure, this section provides workflow diagrams for key processes and a high-level data model of the system. These diagrams will help the team and stakeholders visualize how different components interact and what data entities we need to manage.

_Figure: Typical workflow for creating, reviewing, and sharing a curriculum plan. In this workflow, a **Teacher** begins by creating a new lesson or unit plan using a template in the CMS. The teacher then adds content to the plan (filling in objectives, activities, etc.) and attaches any relevant files or resources. Once the lesson/unit is ready, the teacher shares it through the system – this could be sharing with colleagues for collaboration or submitting to an **Administrator** for review. The **Administrator** reviews the plan, possibly adds feedback or comments, and then approves it. The teacher receives the feedback/approval, makes any needed revisions, and finalizes the plan. The finalized plan is then published in the curriculum repository, making it accessible as appropriate (e.g., visible to other teachers in the department). Optionally, the teacher can push the lesson content out to an LMS or notify students. Finally, **Students** and other stakeholders (with permission) can view the published materials via the LMS or a read-only portal. This end-to-end process ensures quality and collaboration at each step of curriculum planning._

In the above workflow, note how the system facilitates a loop of feedback between teacher and administrator, and then dissemination to students via integration. The workflow can be customized depending on the school’s needs (for example, some schools might skip formal admin approval for each lesson, making that step optional).

Another important perspective is understanding the **data model** – the key entities (objects) in the system and their relationships. Below is a conceptual data model diagram:

_Figure: Conceptual data model for the Curriculum Management System, showing main entities and their relationships. The core entity is a **Course** (also referred to as Subject/Class in context), which is the container for curriculum content for a given subject and grade. Each Course consists of one or more **Units** (represented by the “1.._ units” relationship from Course to Unit), and each Unit consists of one or more **Lessons** (“1.._ lessons”). A **Lesson Plan** can have multiple **Attachments** (files or media) associated with it (“0.._ attachments” from Lesson to Attachment).

Users (teachers or admins) are associated with Courses – a Teacher is typically “assigned to/owns” a Course (or multiple courses), meaning they are responsible for planning that course. Administrators might also be linked to courses in an oversight role (or have global access).

The system also uses **Templates** for lessons and units. A Template defines the structure for those plans. In the model, Template is related to Unit and Lesson (format for unit/lesson), indicating that a Lesson “uses” a Lesson Template and a Unit uses a Unit Template (this could be the same Template entity configured differently, or separate types).

Optionally, the model includes **Learning Standards** – an entity representing educational standards or objectives. Lessons can be aligned to many Standards, and each Standard can be addressed in many Lessons (hence a many-to-many relationship, shown with crow’s foot connectors on both ends). This alignment is an important part of curriculum mapping.

The diagram shows a **User** as a single entity with a role attribute (Teacher or Admin). In practice, user roles will determine what they can do with these entities (e.g., a teacher can create and edit lessons for their course; an admin can read all lessons and create templates, etc.).\*

This data model guides how we will design the database schema and object relationships in code. For instance, we expect tables or collections for Users, Courses, Units, Lessons, Attachments, Templates, Standards, and possibly linking tables for many-to-many relationships (like Lesson_Standards). It’s crucial to get these relationships right to support features like sharing (which might link Users to Courses in different ways) and integration (which might attach additional data like an LMS ID to a Course or Lesson).

**Data Considerations:**

- Each entity will have certain attributes: e.g., Lesson will have title, date, content fields for each template section, etc. Unit will have a title, description, etc.
- Attachments will store metadata like filename, file type, maybe a link or path to the file storage, and which lesson/unit it’s linked to.
- Standards might be stored in a separate reference table with fields like code (e.g., “CCSS.MATH.5.NBT.A.1”) and description, and possibly a hierarchy if we include standard sets.
- Templates will include the definition of sections (which might be stored as a JSON structure or relationally as well).
- We also might have an entity for “Group” or “Department” to manage sharing in groups, but that can also be implicitly managed by sharing to multiple users or a role.

The relationships depicted ensure that when we retrieve a course, we can also fetch its units and lessons easily, or when a teacher logs in, we know which courses (and thus which content) to show them. It also shows that multiple teachers could collaborate on one course (for team-teaching or shared curriculum), since the User-Course link can be many-to-many (one course can have multiple assigned teachers/editors, one teacher can have multiple courses).

**Workflow Diagrams for Integrations:** (Not drawn here, but conceptually)
We could also imagine a flow for integration events. For example, a nightly job workflow: SIS → (roster sync) → CMS updates classes; or Teacher → (push lesson) → LMS via API → LMS confirms. These can be detailed in the Integration section if needed for implementation clarity.

By referring to these diagrams during development, the team can ensure consistency in understanding how data flows through the system and how the objects relate. It’s often helpful to refine these models as we delve into edge cases or additional features.

## Integration Requirements and APIs

Integration with existing educational technology systems is a core requirement for this CMS. The goal is to prevent data silos and duplicate data entry by connecting the curriculum management platform with the school’s **LMS, SIS, and grade book systems**. This section details the integration points, standards to use, and API requirements for both consuming external services and providing our own.

### LMS Integration

- **LMS Integration Scope:** The CMS will integrate with Learning Management Systems such as Canvas, Google Classroom, Schoology, Moodle, or others commonly used. The primary use-cases are: single sign-on, publishing content to the LMS, and possibly embedding the curriculum tool inside the LMS.
- **Single Sign-On via LMS:** If teachers launch the CMS from within an LMS (like an external tool), support the **LTI (Learning Tools Interoperability) standard**. The CMS should function as an LTI 1.3 tool provider so that it can be added to LMS courses. This would allow, for example, a teacher in Canvas to click a “Curriculum Planner” link and be logged into the CMS without separate login ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=LTI%20Integration)).
- **Google Classroom Integration:** Given many schools use Google Classroom, the CMS will have specific integration: teachers can import Classroom class lists (if not via SIS already) and directly post assignments or materials to Classroom from the CMS ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=,Atlas%20to%20your%20Google%20Classroom)). This may use Google Classroom APIs to create course work or materials.
- **Content Publishing:** For LMS like Canvas/Schoology, the CMS could export a lesson in Common Cartridge format or use the LMS’s API. E.g., use Canvas API to create a Page or Assignment with content from the lesson plan (excluding any teacher-only notes). For Google Classroom, use its API to create an “Announcement” or “Assignment” linking attached files.
- **LMS Gradebook:** If we push assignments, also push assignment metadata (due date, points possible) to the LMS’s gradebook. If LTI Advantage’s Assignment and Grade Services are available, consider implementing that for a seamless gradebook connection. For Phase 1, this might be optional.
- **Embedding and Visibility:** Perhaps allow that some curriculum content can be made visible to students via the LMS. For example, a unit overview could be shared as a page in the LMS for students/parents to see. We need to ensure only appropriate sections are shared (maybe a flag on sections whether they are student-facing).
- **Testing & Compatibility:** We will prioritize integration with 1-2 LMS in initial implementation (say Google Classroom and Canvas, as they cover large user bases). The system should be designed such that integration with additional LMS can be added by writing new connectors rather than changing core code.

### SIS Integration

- **Class Roster and Schedule Sync:** Use the school’s **Student Information System (SIS)** to get teacher-course assignments, course titles, student rosters, and timetable information. The industry standard for this is **OneRoster (by IMS Global)**, which defines APIs for roster, course, enrollment data ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=OneRoster%20Ready)). If the SIS supports OneRoster API (or CSV), the CMS should consume that.
- **Data Imported:** Course info (course name, course ID, academic term), Staff info (teacher names, IDs and their course assignments), Student info (if needed; we might not import all student personal data unless needed for something like differentiation notes). Mainly teacher->class relationships and class->schedule slots.
- **Schedule Integration:** If the SIS provides a schedule (like when each class meets), we could integrate that to auto-populate lesson dates or connect with calendar. At minimum, knowing the term start/end dates for a course will help in structuring units and lessons on the timeline.
- **Updating Data:** If a teacher or class assignment changes in SIS, an update should reflect in CMS (could be via nightly sync or real-time if SIS pushes events). The integration should gracefully handle when a teacher leaves or a class is removed (perhaps archive those plans but keep data).
- **Technical Approach:** We will likely implement a scheduled job that calls the SIS API (or processes an uploaded file) to sync data. Admins should have an interface to initiate a manual sync if needed and to view last sync status.
- **Student Data & Privacy:** If roster data (student names, IDs) are pulled in, we must ensure that student personal data is protected (FERPA compliant). Possibly encrypt or at least restrict who can see student names in the CMS (maybe only that teacher in attendance context, but since CMS is for planning, student info might not be displayed at all, which could be simpler from a privacy standpoint).

### Gradebook Integration

- **Standalone Gradebook Systems:** Some schools use SIS as gradebook, others use LMS, and some have separate (e.g., PowerSchool, Gradebook software). Direct integration to external gradebook can be complex. Our strategy:
  - If the LMS is the gradebook (e.g., Canvas), then the LMS integration covers it.
  - If SIS is the gradebook (like PowerSchool), we might rely on SIS integration or OneRoster’s grades extension to push assignment scores.
- **Push Assignments:** At least, ensure we can push assignment definitions to the gradebook. OneRoster has an Assignments and Grades service that could be leveraged if target systems support it.
- **No Pulling Grades Initially:** We likely won’t pull back student scores into the CMS, since it’s out of scope to track student performance here (and could create a FERPA issue storing that data). The integration is one-way: from curriculum plan to gradebook system.
- **Gradebook APIs:** If needed, implement specific API connectors for common gradebook platforms (for example, PowerTeacher Pro API for PowerSchool). This might be in a later phase. For MVP, a simpler approach is allow export of an assignment list as CSV which an admin can import to a gradebook, though that’s not ideal user experience.

### Authentication and User Provisioning

- **SSO Providers:** As mentioned, Google and Microsoft O365 SSO will be supported out of the box ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=Single)). Also, support **Clever** and **ClassLink** which are popular in K-12 for single sign-on (Clever also provides roster data).
- **Local Login (fallback):** In case an institution doesn’t have those, the system can have its own login with username/password, but this is secondary. If used, it should allow an admin to set initial passwords or invite users. Password complexity and reset flows need to be included.
- **User Provisioning:** If SSO is used and roster data is synced, user accounts can be auto-created when data comes in (e.g., if SIS says teacher John Doe teaches class X, then create a user John Doe if not existing, and map his SSO ID). Alternatively, initial user load can be done by an admin via CSV. The integration piece is making sure we don’t require manual user creation. Use of standard SSO (OAuth with Google, etc.) will link to an email domain or specific allowed domains.

### API (Provided by CMS)

- **Public API Endpoints:** The CMS should offer a RESTful API (with JSON responses) for key resources: courses, units, lessons, standards, attachments metadata. This would allow other software or scripts to query curriculum data. For example, an admin might want to retrieve all lesson titles for a course via API to generate a custom report.
- **API Security:** The API should require authentication (likely using API keys or OAuth tokens). Each API call should enforce permissions (so only an admin token can retrieve all courses, a teacher token only gets their courses, etc.). If building an external developer API, we could implement OAuth2 with client credentials or similar.
- **Use Cases for API:** Potential uses include integration with district data warehouse, enabling a mobile app in future, or third-party tools that want to pull our curriculum data (maybe a parent portal that shows what’s being taught – they could call our API for the public view of curriculum).
- **APIs for Importing:** In addition to output, if a district has existing curriculum in another format, having an import API or script could help migrate data. This might be more one-time than a continuing integration.

### Data Standards and Format

Where possible, adhere to known standards:

- **OneRoster:** for roster and course data.
- **LTI 1.3 / LTI Advantage:** for LMS launch and integration.
- **Common Cartridge or Thin Common Cartridge:** for exporting content in a standardized e-learning content package (this could allow an admin to export all lesson content and import into another system if needed).
- **Ed-Fi (less common for curriculum)**: Some districts use Ed-Fi data standard. Not a priority unless specifically needed.

### Integration Configuration:

- Provide an **Integration Settings UI** for admins: e.g., fields to enter their SIS API credentials, toggle Google Classroom integration on/off, etc. Logging and error handling: if an integration sync fails (e.g., SIS unreachable), the admin should get an error message/log to troubleshoot.

### Testing Integrations:

- Each integration (SIS, LMS) must be tested in a staging environment with dummy data to ensure it doesn’t corrupt real data. We should consider offering a sandbox mode or dry-run for initial setup.
- Also, backward compatibility: e.g., if the school changes SIS or LMS, how easily can we reconfigure? Ideally, keep things modular.

By fulfilling these integration requirements, the CMS will fit smoothly into the existing workflow of educators who already use SIS for class info and LMS for delivering content. It will act as the planning brain that connects to those systems, thereby improving efficiency and data consistency ([Choosing the Best Curriculum Software [How To + Features]](https://akarisoftware.com/2023/12/20/curriculum-management-software/#:~:text=A%20crucial%20aspect%20of%20a,as%20SIS%2C%20LMS%2C%20and%20ERP)) ([Choosing the Best Curriculum Software [How To + Features]](https://akarisoftware.com/2023/12/20/curriculum-management-software/#:~:text=Integrations%20with%20SIS%2C%20LMS%2C%20ERP)). Importantly, using standards (LTI, OneRoster) will make implementation easier and future-proof (ease of implementation and maintenance), leveraging already available libraries and reducing custom work.

## Security and Compliance Requirements

Security and regulatory compliance are paramount, given that the system will handle educational records, user information, and possibly student data. This section enumerates requirements to ensure the system is secure against unauthorized access and compliant with relevant policies and laws (especially in the education domain).

**1. User Authentication & Authorization:**

- The system must authenticate every user who accesses it. For web UI, that means secure login (preferably via SSO as noted earlier). For APIs, that means token-based auth.
- **Session Management:** Use secure cookies for sessions, with appropriate expiration and idle timeouts (e.g., auto-logout a user after a certain period of inactivity, perhaps 1-2 hours, to prevent someone inadvertently staying logged in on a public computer).
- Authorization checks on all actions: e.g., only the owner or shared collaborators of a lesson can edit it, only admins can access admin functions. This should be enforced server-side (never rely solely on hiding buttons in the UI).
- Implement least privilege: ensure that if a user somehow tries to escalate privileges (e.g., by API calls), the system prevents it. Regular users should not be able to hit an admin endpoint, etc.

**2. Data Privacy (FERPA/GDPR Compliance):**

- **FERPA:** The Family Educational Rights and Privacy Act in the U.S. requires that student information is protected and only accessible to those with legitimate educational interest. In our context, student info might only be rosters (names, IDs) if even used. Ensure that student roster data is only visible to the teachers of those students and relevant admins. Perhaps avoid storing sensitive student data in CMS at all beyond names/IDs, which simplifies compliance.
- The system should log access to student data (who viewed or downloaded something with student info, if applicable).
- If any student performance info were to be stored (e.g., teacher notes about a student in a lesson plan), that becomes part of educational record and must be protected similarly.
- **GDPR:** If any users (teachers) are in the EU or if the product is international, comply with data protection principles: have clear consent for any personal data stored, provide ability to delete personal data if a user leaves (e.g., if a teacher account is removed, personal identifying info can be deleted, though their contributed curriculum might be retained as institutional data but anonymized).
- **Data Minimization:** Only collect and store data that is needed for the product functions. For example, we don’t need student birthdates or addresses, so we should not store them. Limit personal info to what’s needed (names, emails for login, etc.).
- **Privacy Policy:** Ensure there is a documented privacy policy and possibly a FERPA disclosure if this is a product for schools, so administrators know how data is handled. (This is more a business/legal requirement than system, but the system should be built in line with the promises made).

**3. Data Security Measures:**

- **Encryption:** As noted, enforce HTTPS for all client-server communication. If any sensitive data is stored (like integration API keys, passwords for local accounts), encrypt them in the database. For example, use encryption for API tokens for SIS if we store them, or at least store in a secure vault.
- **Penetration Testing & Vulnerability Scanning:** The application should undergo routine security testing. Use automated tools to scan for SQL injection, XSS, CSRF vulnerabilities, etc. All forms and inputs must be validated and escaped to prevent these attacks.
- **CSRF Protection:** Use anti-CSRF tokens in forms or same-site cookies to prevent cross-site request forgery on authenticated actions.
- **Content Security Policy (CSP):** Implement CSP headers to mitigate XSS by controlling sources of scripts if possible.
- **Password Policy (if applicable):** If local accounts exist, enforce a strong password policy (min length, complexity, etc.) and provide multi-factor authentication for admin accounts if possible for extra security.
- **Audit Logging:** Keep an audit log especially for critical actions: user login/logout, creation/deletion of major entities (courses, units, etc.), sharing events, permission changes, and integration operations. Logs should include who did what and when. These logs should be secure (non-editable by normal users) and retained for a period (e.g., one year) for forensic purposes if needed.
- **Data Backups & Recovery:** From a security standpoint, ensure backups are also secured (encrypted at rest, stored in a secure location). A breach in backups is as bad as production if not protected. Also, have a disaster recovery plan – e.g., how quickly can we restore service if the database crashes (Recovery Time Objective), and how much data could we lose at most (Recovery Point Objective, e.g., 24 hours if daily backups).

**4. Compliance and Standards:**

- If the product will undergo any certifications (like SOC 2, ISO 27001 eventually), design with those controls in mind (e.g., access controls, change management, etc.). Not required at BRD stage, but good to note that such compliance might be a goal.
- **COPPA:** If any part of the system becomes accessible to students under 13 (e.g., if a student view is provided), then compliance with COPPA (Children’s Online Privacy Protection Act) is needed. This means obtaining parental consent via the school and not collecting more info from children than needed. But likely our primary users are teachers/admins, so this might not apply directly unless we add student accounts.

**5. Environment and Deployment Security:**

- If on cloud, ensure the cloud environment is securely configured (VPC, firewalls only allowing necessary ports, etc.). Use separation of environments (dev/test/prod) to prevent test code or users affecting prod data.
- The system should have the ability to handle data jurisdiction – e.g., host EU school data in EU if needed (depending on product scope). This is advanced, but mention if compliance may require it (for GDPR, data residency can be an issue if we host everything in US but have EU users).

**6. User Role Restrictions:**

- Specific to our domain: a teacher should not be able to change their role or elevate privileges. Admin accounts creation should itself be restricted. Possibly implement two-factor auth for admin users to mitigate risk of admin account compromise.
- Ensure that when a teacher leaves (account deactivated), their curriculum data can either be transferred to another or at least remain accessible to admins. (This touches data ownership – often the school owns the lesson plans, not the individual teacher, so admins should always have access even if teacher account is gone.)

**7. Compliance with Accessibility (Section 508):**

- Since it’s for education, if any federal funding or public school usage, it typically needs to meet accessibility standards (often Section 508 in the US, which overlaps with WCAG). We covered that in UI/UX but we can reaffirm that compliance with accessibility guidelines is both a quality and a legal compliance matter.

In summary, security and compliance require a combination of good system design, careful coding practices, and operational policies. The development team should integrate these requirements from day one (security by design, privacy by design) rather than as an afterthought. We will also involve the district IT/security team to review our approach and ensure it aligns with their expectations (for example, some districts might have a security questionnaire or require certain cloud controls before approving the tool). Meeting these requirements not only avoids legal issues but also builds trust with users (teachers/admins will trust the system to hold their work safely and privately).

## Implementation Roadmap

Delivering a complex system like this CMS will require a phased approach. The following implementation roadmap breaks down development into phases with a focus on delivering core value early (to get feedback and adoption) and then iterating with additional features. The roadmap also highlights how we will prioritize **internal collaboration** (both in terms of the product features and the development process) and **ease of implementation** (choosing standards and existing solutions to accelerate progress).

### Phase 1: **MVP – Core Planning and Sharing (Months 0–6)**

**Goal:** Deliver a Minimum Viable Product that includes the essential features for lesson planning and basic collaboration, allowing a pilot group of teachers to start using the system and providing feedback.

- **Features in Phase 1:**
  - Basic **Lesson Plan Editor with Templates**: Implement one or two fixed templates initially (e.g., a basic lesson template with key fields). Allow teachers to create/edit lessons and save them. Include attachments and standards tagging for lessons ([Planbook - The Leader in Lesson Planning](https://planbook.com/#:~:text=,repository%2C%20or%20add%20your%20own)).
  - **Unit and Course structure:** Allow organizing lessons into units and units into a course. The UI can be simplified (maybe an outline view without the full visual timeline at first, but ensure the hierarchy works).
  - **User Accounts & Auth:** Set up SSO (likely Google to start, as many pilot schools use Google Workspace) for login ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=Single)). Create basic user management for admin to assign roles.
  - **Collaboration – Sharing & View:** Enable teachers to share lessons or units with others in view-only mode. Possibly enable edit sharing for small pilot (maybe just one person editing at a time to avoid complexities initially).
  - **Basic Commenting:** Provide ability to comment on a lesson (even if just a single discussion thread per lesson to start with).
  - **SIS Import (One-time):** Instead of full integration, do a one-time import of teacher-course mappings to set up courses in the system (to avoid manual course creation). This could be via CSV or a quick integration if easy (maybe using a sample OneRoster file).
  - **No LMS integration yet in MVP**, except perhaps a simple export (PDF export of a lesson).
  - **Initial UI:** Focus on making the lesson editor and course view usable and clean. It’s okay if some advanced UI (like drag-and-drop scheduling) isn’t there yet. Use a proven rich text editor component for the lesson fields to save time (ease of implementation).
- **Internal Implementation Considerations:**
  - We will use an **agile approach** with iterative sprints (~2 weeks each). Early sprints will focus on setting up the backend (data model, APIs) and a very rough UI. By sprint 3 or 4, we should have a working slice: e.g., create course, add lesson, share lesson.
  - **Leverage frameworks/libraries:** To speed up development, use existing libraries for things like rich text editing (e.g., Quill or TinyMCE), file uploads (AWS S3 or Google Cloud Storage SDKs for backend), and authentication (OAuth libraries). Using these will accelerate development and ensure reliability (ease of implementation through not reinventing the wheel).
  - **Collaboration within Dev Team:** Set up regular check-ins with curriculum specialists (domain experts) in the team to validate that what we build meets actual needs. Possibly have a few friendly teachers try an early prototype (internal UAT) around month 3.
- **Deliverable & Testing:** By the end of Phase 1, we aim to have a pilot-ready system. We’ll conduct an internal QA and also a pilot with, say, one school or a small group of teachers who will use the system for a few weeks. Their feedback will be crucial for Phase 2 priorities.
- **Success Criteria for Phase 1:** Teachers can create, save, and view lesson plans and share them with an admin who can view and comment. The system remains stable with ~10-20 concurrent users (pilot scale) and positive feedback that it indeed saved them some time or made planning more organized.

### Phase 2: **Enhanced Collaboration and Mapping (Months 6–12)**

**Goal:** Build on the MVP by adding the comprehensive curriculum mapping features and stronger collaboration tools, and begin integrating with external systems.

- **Features in Phase 2:**

  - **Curriculum Mapping Visualization:** Implement the more advanced course map view (timeline/calendar for units) and the ability to plan out the schedule (e.g., assign dates/durations to units and lessons, maybe integrate a calendar) ([OpenCurriculum: Lesson planning, unit planning, and curriculum mapping and alignment software for K-12 schools tools](https://opencurriculum.org/#:~:text=Track%20your%20long,plans%20visually)). Include a “scope & sequence” report or at least a printable overview of the course.
  - **Template Customization UI:** Allow admins to create/edit templates rather than having them fixed. This includes adding/removing sections and setting default text ([Planbook - The Leader in Lesson Planning](https://planbook.com/#:~:text=Flexible%20Lesson%20Templates)).
  - **Advanced Sharing:** Add group sharing (departments, PLC teams) and permission levels (edit vs view) ([Planbook - The Leader in Lesson Planning](https://planbook.com/#:~:text=,lessons%2C%20viewable%20only%20by%20you)). Possibly implement real-time co-editing if feasible (using something like operational transforms or leveraging a collaboration-friendly editor).
  - **Approval Workflow:** If there is demand from pilot feedback, introduce the ability for an admin to mark lessons approved and maybe a status indicator for lessons (draft/ready/approved). Use the Planbook idea of status tags or similar functionality ([Planbook - The Leader in Lesson Planning](https://planbook.com/#:~:text=,your%20classes%20and%20lesson%20sections)) ([Planbook - The Leader in Lesson Planning](https://planbook.com/#:~:text=,your%20classes%20and%20lesson%20sections)).
  - **Search Functionality:** Implement global search for lessons/units by text and filter by metadata (this might have been partially present in MVP, but here we refine it with indexing).
  - **Integration – Phase 2:**
    - Start working on **LMS integration** for one platform (Google Classroom integration likely first, since it’s straightforward using Google APIs, to push assignments ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=,Atlas%20to%20your%20Google%20Classroom))).
    - **SIS Integration** automated: Implement a scheduled job to sync with SIS (if OneRoster API available, use it now). If pilot district uses Clever, integrate with Clever to pull class data.
    - Basic **SSO with Microsoft** as an additional option if there are schools using O365.
  - **Improved Attachments:** Possibly integrate with Google Drive picker ([Features - Atlas](https://www.onatlas.com/atlas#:~:text=Google%20Suite%20for%20Education%20Integration)), so teachers can attach files from Drive easily (since that’s common in schools).
  - **Analytics (basic):** Add simple reports for admins, like listing all courses and how many lessons each has, or which standards aren’t used. Not full analytics module, but a start.

- **Internal Focus:**

  - Incorporate pilot user feedback from Phase 1 extensively. If teachers said navigation was confusing, improve that in this phase. Maybe conduct a design review before implementing the new UI elements (collaborate with a UX designer).
  - Ensure the development team is subdivided if needed: e.g., one sub-team works on core UI improvements, another on integration back-end, to parallelize work.
  - Prioritize features that improve **collaboration** (since the prompt emphasizes internal collaboration) – e.g., real-time editing and comments are big ones in this phase. These will make the product much more engaging for multiple users.
  - Also, from an engineering perspective, ensure we refactor any quick hacks from Phase 1 into more robust code in Phase 2, knowing the user base might grow.

- **Testing & Deployment:** By end of Phase 2 (around month 12), we should be ready to onboard more schools or the entire district. We’ll do performance testing to ensure the system can handle say 100+ users concurrently (some scaling testing). Also test integration flows thoroughly (especially anything writing to LMS or pulling from SIS).

  - Likely do a Beta release to a larger group of teachers and possibly allow them to start migrating their existing plans into it for a new school year.

- **Success Criteria for Phase 2:** The system is fully adopted in the pilot school for daily lesson planning; at least 80% of teachers are actively using it to write their plans each week. Administrators are using the system to review plans rather than email spreadsheets. Integration with Google Classroom is working, saving teachers time posting assignments. Feedback should indicate that the tool has improved collaboration (e.g., teachers sharing more plans with each other). Also, we should see a reduction in redundant work – perhaps measured by instances of teachers reusing or adapting each other’s shared lessons.

### Phase 3: **Integrations and Advanced Features (Months 12–18)**

**Goal:** Expand the system’s capabilities with deeper integrations and nice-to-have features, and prepare the product for a wider rollout beyond the initial context (making it more generic, multi-tenant, etc., if needed).

- **Features in Phase 3:**
  - **Additional LMS integrations:** Based on demand, add integration for one or two more LMS (for instance, Canvas or Schoology via LTI/API).
  - **Gradebook Integration:** If not yet, implement connection to SIS gradebook (e.g., pushing assignment data to PowerSchool). Possibly pilot this with a small subset of data to ensure it works correctly.
  - **Mobile-Friendly Enhancements:** Perhaps develop a simplified mobile view or companion app for quick viewing of lesson plans by teachers on the go.
  - **Complete Analytics Module:** Provide a section for curriculum analytics: e.g., coverage of standards by course, identify unused standards, comparison of plans across years, etc. Also, a collaboration analytics (like which teachers are contributing or sharing the most, to identify champions or needs).
  - **Multi-school/District Support:** If this product is to be rolled out across multiple schools or a whole district, ensure the architecture supports multiple schools’ data segregation. That might involve adding a School entity and scoping users to it, etc. In a single-school pilot, this wasn’t needed, but for larger adoption, handle that (ease of implementation here if we planned well initially with a tenant ID).
  - **Archiving and Cloning Curricula:** Add features to archive last year’s plans, and roll over or copy a course for a new year. Teachers often like to start from last year’s plan and tweak, so implement a “clone course” function that copies all units and lessons (without student data obviously) to a new instance for the new academic year.
  - **Polish & UX tweaks:** Based on broader user feedback, refine any UI issues, improve load times further, add convenience features (like drag-drop reordering, bulk actions such as shifting dates of multiple lessons).
- **Internal Process in Phase 3:**

  - By this stage, we should have a stable core. Phase 3 might involve increasing the team if we want to accelerate new features (especially if the product is a success and more requests are coming).
  - Keep in mind **ease of maintenance**: as features pile on, ensure we maintain code quality, add automated test coverage, and possibly start writing more formal documentation (for both internal dev and external user guides).
  - Plan for training and support: internal team might need to prepare to hand off to a support team if scaling to many schools.

- **Deployment:** After Phase 3, we should be ready for full launch across the intended user base (which could be an entire district or selling as a product to other districts). We might set up a cloud environment that can host multiple instances, etc.

  - We will also likely set up continuous deployment pipelines by now for smooth updates, as the software will be in active use and we may do frequent minor releases with improvements.

- **Success Criteria for Phase 3:** The system successfully integrates into all needed systems such that teachers no longer have to manually duplicate content into LMS or gradebook – at least a 50% reduction in such double-entry tasks. The majority of planning work is done in the CMS. If surveyed, at least e.g. 70% of teachers agree that “The CMS has improved our curriculum planning process.” The district leaders see improved alignment and easier reporting on curriculum. Also, from a technical perspective, the system can handle the full load (e.g., all schools in the district using it simultaneously).

### Future Considerations (Beyond 18 months):

- **AI Assistance:** Possibly integrate AI features (e.g., suggest resources for a lesson, auto-generate a first draft of a lesson plan given a topic) – there are emerging tools in this area. Not in initial scope, but an area to explore once core system is in place.
- **Community Sharing:** Allow teachers to share certain curriculum publicly or across districts (if the product goes broader, could have a repository of teacher-contributed lessons similar to OER platforms).
- **Additional Compliance:** If expanding globally, adapt to different standards sets (like different state standards, national curricula).
- **Continuous Improvement:** Establish a feedback loop where each semester we gather user suggestions and feed that into the next update cycle (perhaps via a user group or regular surveys).

Throughout these phases, we prioritize tasks that deliver the highest impact first (e.g., planning and sharing features early, integrations later once basic workflow is solid). We also take into account **ease of implementation**: for example, using well-documented APIs and libraries (Google API, OneRoster) rather than building custom solutions from scratch, which speeds up integration development. Internal collaboration is fostered by building features that encourage teachers and admins to work together (sharing, commenting) early on, and by ensuring our development process is collaborative (regular demos to stakeholders, involving actual users in testing).

The roadmap is a guiding plan; we will remain agile and adjust timelines or feature priorities based on user feedback and any new constraints (e.g., if a mandate comes that all lessons must be aligned to standards by next year, we’d ensure that standards reporting gets prioritized). The incremental approach mitigates risk and allows the project to deliver value at each milestone, rather than a big bang release after a long development with no user input.

## Success Metrics and KPIs

To measure the success of the Curriculum Management Software, we will track several **Key Performance Indicators (KPIs)** and metrics aligned with the project’s objectives. These metrics will help the internal team understand how well the system is being adopted, how it is improving the curriculum process, and where further improvements or changes might be needed. Below are the critical success metrics:

**1. User Adoption and Engagement:**

- **Percentage of Teachers Actively Using the System:** For example, the number of teachers who login and create or edit at least one lesson plan per week vs. the total number of teachers. A high adoption rate (e.g., >85% of teachers using the tool weekly) would indicate success in becoming a part of their routine.
- **Daily/Weekly Active Users (DAU/WAU):** Track the active user counts to ensure consistent usage, not just one-time logins. If WAU is low, it means teachers might be falling back to old methods.
- **Plans Created per Teacher:** An average number of lesson plans created per teacher per month. If teachers are supposed to do one per day, we’d expect ~20 per month in a fully adopted scenario. If initially we see less, that might indicate partial use or lingering use of other tools.
- **Time Spent in Application:** If we can gather analytics, how much time (on average) a teacher spends in the CMS per planning session. Ideally, it should show efficiency gains over time (e.g., it might take a teacher 2 hours to plan a week initially, but after templates and reuse, it might drop).

**2. Collaboration and Sharing Metrics:**

- **Number of Shared Curriculum Items:** How many lessons/units are shared among teachers. Growth in sharing indicates that teachers trust and use each other’s work (e.g., “X% of lesson plans are shared with at least one other colleague”).
- **Peer-to-Peer Collaboration Rate:** Could be measured by the number of comments or co-editing instances. For example, how many lessons have comments from a different user than the author, or how many have multiple editors. A high collaboration rate suggests the system is facilitating teamwork.
- **Administrator Review Completion:** If an approval workflow is in place, measure what proportion of submitted plans get reviewed/approved by admins in a timely manner (e.g., within 2 days). If the system is working, we’d expect near 100% of required plans are being reviewed via the system rather than outside it.
- **Content Reuse Rate:** Instances of teachers copying or importing existing shared lessons for their own use. This indicates reduction of duplicate effort. E.g., “25 lessons were reused from the shared library this semester, saving an estimated Y hours of work.”

**3. Curriculum Quality and Alignment (Outcomes):**

- **Standards Coverage:** Track the percentage of required standards that have at least one lesson aligned in the system. For instance, if a curriculum has 100 standards and initially only 50% were documented as covered, after using the CMS it might rise to 90% coverage because teachers are more aware and the system reminds them of alignment. High coverage indicates better alignment of taught curriculum to required standards ([21 Best Curriculum Management Software for 2025 | Research.com](https://research.com/software/best-curriculum-management-software#:~:text=Curriculum%20management%20platforms%20facilitate%20the,software%20to%20properly%20manage%20documents)).
- **Curriculum Gap/Overlap Reduction:** If we implement analytics, we could measure if redundancies (same standard hit too often) or gaps (standards never addressed) decrease over time across the curriculum. This would come from reports and show improvement in mapping.
- **Teacher Satisfaction/Feedback:** Through surveys or feedback forms: e.g., “What is your satisfaction with the curriculum planning process now vs before?” – aiming for a positive increase. A specific metric could be “% of teachers who say the CMS has made planning easier” with a target like > 80%.
- **Quality Observations:** Although qualitative, admins could note if lesson plan quality (completeness, thoughtfulness) has improved now that templates and feedback are in place. Possibly track the number of plans that meet all required components without revision – aiming for improvement.

**4. Efficiency and Time Savings:**

- **Reduction in Planning Time:** We can attempt to measure via survey or observation how much time teachers spend planning now versus before using the tool. For example, if baseline was 9 hours per week on curriculum tasks ([21 Best Curriculum Management Software for 2025 | Research.com](https://research.com/software/best-curriculum-management-software#:~:text=Teachers%20also%20spend%20a%20significant,Learning%20Counsel%2C%202021)), can we reduce that significantly (even anecdotally)? If teachers report “I save 2 hours a week using the CMS,” that’s a big win.
- **Faster Onboarding of New Teachers:** A metric could be how quickly a new teacher can get up to speed by using existing curriculum in the system. If, for instance, new hires use the system to access last year’s plans and thereby spend less time in preparation their first year, that’s a success (could measure via a survey question like “The curriculum system helped me prepare to teach new content – agree/disagree”).
- **Administrative Efficiency:** How much time admins spend gathering curriculum info for reports or audits. If previously they had to collect documents from teachers, and now they can just run a report, measure that reduction. For example, “Time to compile curriculum alignment report” from days to minutes.

**5. Technical Performance Metrics:**

- **System Uptime:** Track uptime; target 99% or above during working hours. Any major downtime incidents count against success until resolved.
- **Response Time:** Average page load or action execution times from user analytics. We set a threshold (like <3 seconds for page loads, <1 second for most interactions) and track percentage meeting that. If performance dips (especially under load at peak times), that’s a red flag to address.
- **Issue Tickets/Support Requests:** Number of support issues or bug tickets logged by users. If after rollout, the number of issues per user is low and trending downward, that indicates stability and ease of use. If we see recurring problems (like many “how do I do X” questions), that indicates areas to improve in UX or training.

**6. Integration Effectiveness:**

- **SSO Adoption:** Percentage of users logging in via SSO vs manual. Ideally >90% use SSO, indicating smooth integration into their daily login flow.
- **Data Sync Accuracy:** For SIS integration, verify that 100% of active classes and teacher assignments are correctly represented in the CMS. We can cross-check counts (e.g., if SIS has 50 classes, CMS shows 50 classes).
- **LMS Push Usage:** How many times teachers use the “Publish to LMS” feature (if implemented). If this number grows, it’s a sign the integration is useful. Also qualitatively, if teachers say “I no longer upload files to Google Classroom manually, I just do it through CMS,” that’s success.
- **Reduction in Duplicate Entries:** Perhaps measure that no one is manually re-entering data that the integration handles. Could survey: “The integration with [SIS/LMS] saved me time – yes/no.”

**7. Project Delivery Metrics (Internal):**

- Although not product usage metrics, for the internal team we might track if the project stays on schedule and within scope:
  - Hitting phase milestones on time (Phase 1 complete in 6 months, etc.).
  - Budget adherence if applicable (development effort didn’t grossly exceed estimates).
  - Also, the number of change requests or scope creep items – keeping those minimal might indicate the BRD was thorough and on target.

Once the system is in use, we will gather these metrics via analytics tools, database queries, surveys, and feedback sessions. For example, we might implement an analytics dashboard for admin users to see some of these (like adoption, standards coverage).

Crucially, success is not just about numbers but also the overall impact: **Are teachers planning better lessons with less stress? Are students ultimately receiving a more coherent and engaging curriculum?** While student outcomes (like test scores or engagement) are influenced by many factors, a long-term success indicator could be improvement in those areas attributed partially to better curriculum planning. For the scope of this project, we focus on the direct metrics above.

We will review KPIs regularly (e.g., monthly in the first year of deployment) and share with stakeholders to celebrate successes (like high adoption) and identify areas for improvement (for instance, if collaboration metrics are low, we might need to provide more training on sharing features or improve those features). By quantifying our success, we ensure the project stays aligned with its goals and demonstrates ROI to the institution.
