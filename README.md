# The Automobile Management System

This repository contains my **INFO1110 (Introduction to Programming)** project from the **University of Sydney (Semester 1)**, created using **Python**.

This project focuses on designing and implementing a **complete command-line automobile dealership and vehicle management system**, emphasising object-oriented programming, clean software design, scalability, and persistence. The system simulates real-world workflows such as inventory management, vehicle purchasing, ownership, maintenance, and transaction logging.

---

## 📘 Project Overview

At a high level, this project implements a **full dealership-style workflow** through a Python-based CLI application. The system supports multiple vehicle types and user roles, while maintaining persistent data across sessions.

The project includes functionality to:

- Manage a central inventory of vehicles (Cars, Electric Cars, and Bikes)  
- Allow users to create accounts, log in, and purchase vehicles  
- Enable post-purchase vehicle management (driving, refuelling, charging, riding)  
- Provide administrative controls for inventory updates, discount events, and sales reporting  
- Persist inventory, users, owned vehicles, and sales data to disk  

The application is designed to be modular, extensible, and maintainable.

---

## 🌍 Research Focus & Motivation

While primarily a programming project, the motivation behind this system was to simulate **realistic software behaviour** found in inventory-driven applications. The focus was on:

- Translating real-world processes (buying, owning, maintaining vehicles) into code  
- Designing software that remains usable and efficient as data volume increases  
- Applying advanced programming concepts without overcomplicating the system  

This project demonstrates how thoughtful design choices improve clarity, performance, and scalability.

---

## 📊 Analytical Approach

The project prioritises **structured software reasoning** over superficial complexity. Key design decisions include:

- Using **object-oriented inheritance** to model real-world entities  
- Centralising shared state using class variables  
- Applying NumPy for efficient bulk and randomised operations  
- Separating concerns such as logging, persistence, and business logic  

Rather than maximising feature count, the project focuses on **clarity, correctness, and extensibility**, aligning with INFO1110 learning outcomes.

---

## 🧾 Report Production Workflow

The system was developed as a **single cohesive Python application**, structured across two modules:

- `main.py` — handles user interaction, menus, authentication, transactions, and persistence  
- `classes.py` — defines the vehicle hierarchy and reusable decorators  

Key implementation features include:

- Persistent storage using text files for inventory, users, owned vehicles, and sales data  
- Generator expressions for memory-efficient file writing  
- Safe parsing of stored transaction data using `ast.literal_eval`  
- Decorator-based logging to track key actions with timestamps  

---

## 📂 Repository Structure

```text
project_root/
├── main.py
├── classes.py
└── README.md
````

---

## 🧠 Key Learnings

* Designing a scalable object-oriented system using inheritance and class variables
* Using decorators to separate logging from business logic
* Applying **NumPy** for efficient random selection and performance-sensitive operations
* Implementing persistent storage with safe parsing and memory-efficient writing
* Structuring a large CLI application with clean control flow and modular design

---

## 🛠 Tools & Technologies

* **Python**
* **NumPy**
* **Object-Oriented Programming (Inheritance, Class Variables, Special Methods)**
* **Decorators (Centralised Action Logging)**
* **File I/O and Persistent Storage**
* **tabulate (Console Table Rendering)**

---

## 📝 Significance

This project represents a **major step forward from introductory scripting to structured software design**. It reinforced:

* Thinking in terms of systems rather than isolated functions
* Writing maintainable, extensible code
* Making deliberate design decisions to balance complexity and clarity

The concepts applied here form the foundation for larger software and data-driven systems.

---

## 🎓 Course Information

* **University:** The University of Sydney
* **Unit:** INFO1110 – Introduction to Programming
* **Assessment Type:** Programming Project
* **Semester:** Semester 1
