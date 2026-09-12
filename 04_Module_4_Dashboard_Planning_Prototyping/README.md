# Module 4 – Dashboard Planning & Prototyping

## EduVision_DV | Higher Education Performance Dashboard

### 1. Module Overview

Module 4 focuses on **planning and prototyping the EduVision_DV Tableau dashboard suite**.

The objective of this module is to design the structure and user experience of the dashboards before completing the final dashboard development and integration stages.

The dashboard suite is planned around four analytical views:

- University Overview
- Research Analytics
- Student Analytics
- Country Comparison

---

### 2. Module Objectives

The main objectives of Module 4 are:

- Design the layouts for the four dashboards.
- Define the visual structure of each dashboard.
- Identify the required filters and controls.
- Plan dashboard navigation.
- Define dashboard actions.
- Plan interactive comparisons.
- Create a dashboard storyboard.
- Develop an initial Tableau prototype.
- Verify the basic prototype functionality.

---

### 3. Dashboard Planning

The EduVision_DV dashboard suite is planned as four interconnected analytical dashboards.

| Dashboard | Main Purpose |
|---|---|
| University Overview | Analyze overall university ranking and academic performance |
| Research Analytics | Analyze research impact and research productivity |
| Student Analytics | Analyze international students, faculty-to-student ratio, and student diversity |
| Country Comparison | Compare education performance across countries |

---

### 4. Dashboard Layouts

#### University Overview

The dashboard is planned to provide an overall view of university performance, including:

- Top university rankings
- Global university distribution
- Academic reputation analysis
- University performance analysis
- Institutional comparison

#### Research Analytics

The dashboard focuses on research-related performance, including:

- Publications analysis
- Citation performance
- Research productivity trends
- Top research institutions
- Research impact comparison

#### Student Analytics

The dashboard focuses on student-related indicators, including:

- International student analysis
- Faculty-to-student ratio analysis
- Student diversity trends
- Enrollment comparisons
- Student distribution analysis

#### Country Comparison

The dashboard focuses on country-level education analysis, including:

- Country ranking comparison
- Education performance benchmarking
- Regional education trends
- Top-performing countries

---

### 5. Filters and Interactive Controls

The dashboard planning stage defines the interactive elements required for the dashboard suite.

Planned controls include:

- Country filters
- University filters
- Ranking-related filters
- Navigation controls
- Interactive comparisons
- Dashboard actions

These controls are intended to allow users to explore university and country-level education data interactively.

---

### 6. Dashboard Navigation

The dashboard suite is designed with navigation between the major analytical views:

```
                    EduVision_DV
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
University Overview  Research Analytics  Student Analytics
        │                │                │
        └────────────────┼────────────────┘
                         ↓
                  Country Comparison
```

Navigation controls allow users to move between the different dashboard views.

---

### 7. Dashboard Actions

Dashboard actions are planned to support interaction between dashboard components.

The planned interactions include:

- Filtering
- Dashboard navigation
- Interactive comparisons
- Parameter-based interaction where required
- Linking related dashboard views

---

### 8. Dashboard Storyboard

The dashboard storyboard documents the planned structure and visual organization of the EduVision_DV dashboard suite.

The storyboard is stored in:

```
planning/
└── dashboard_storyboard.pdf
```

It provides a visual reference for the dashboard layouts and planned user interactions.

---

### 9. Tableau Prototype

An initial Tableau prototype is created to represent the planned dashboard functionality.

The prototype is stored in:

```
prototype/
└── eduvision_prototype.twbx
```

The prototype is used to verify the planned dashboard structure and basic interactive functionality before full dashboard development.

---

### 10. Repository Structure

```
04_Module_4_Dashboard_Planning_Prototyping/
│
├── README.md
│
├── planning/
│   └── dashboard_storyboard.pdf
│
└── prototype/
    └── eduvision_prototype.twbx
```

---

### 11. Expected Evaluation

According to the project requirements, Module 4 is evaluated based on:

| Evaluation Area   | Target                                  |
|--------------------|------------------------------------------|
| Dashboard Design   | Designs approved                        |
| Prototype          | Functionality verified                  |
| Dashboard Layouts  | Four dashboards planned                 |
| Interactivity      | Filters, navigation, and actions planned |

---

### 12. Module Outcome

At the completion of Module 4, the structure and interaction design of the EduVision_DV dashboard suite are established.

The storyboard and prototype provide the foundation for the next development stage:

**Module 5 – Dashboard Development**

where the University Overview and Research Analytics dashboards are developed using Tableau.