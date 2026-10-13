# CareFlow: Clinical Pathway Process Mining

## 1. Project Overview
CareFlow is a clinical process analysis system designed to study patient care pathways using clinical event logs. It helps identify the actual sequence of clinical activities, compare patient pathways, and detect deviations from an expected workflow.

## 2. Problem Statement
Clinical activities may occur in different sequences across patient cases. Understanding these variations manually can be difficult. CareFlow aims to organize clinical event data and provide a systematic way to analyze care processes and identify pathway deviations.

## 3. Project Objectives
- Store and process structured clinical event data.
- Represent patient pathways as sequences of clinical activities.
- Discover common activity sequences and process patterns.
- Identify deviations from a defined expected pathway.
- Visualize process analysis results through a dashboard.

## 4. Proposed Core Features
1. Clinical event data import
2. Patient case and activity timeline
3. Process pathway visualization
4. Expected-versus-actual pathway comparison
5. Deviation identification and reporting
6. Analysis dashboard

## 5. Proposed Technology Stack
- Frontend: React
- Backend: Python with FastAPI
- Database: PostgreSQL
- Process mining: PM4Py
- Version control: Git and GitHub

These technologies are proposed and can be adjusted if implementation requirements change.

## 6. Data Structure
The initial event log will use synthetic data and include:
- Case ID
- Activity name
- Activity timestamp
- Activity sequence
- Optional department or resource field

No real patient-identifiable data will be used during initial development.

## 7. Initial System Workflow
1. Import or load sample clinical event data.
2. Validate and prepare the event log.
3. Group events by case and sort them by timestamp.
4. Analyze activity sequences and pathway variations.
5. Display findings in a dashboard.

## 8. Week 1 Goals
- Understand the process mining concept.
- Define project objectives and core features.
- Design the initial event log structure.
- Prepare synthetic sample data.
- Establish the initial project structure.
- Document progress and commit completed work to the assigned GitHub branch.

## 9. Future Scope
The system may later support more advanced process mining techniques, additional visualizations, and expanded analysis features.