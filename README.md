# lab

This repository collects all of my small learning and practice projects, grouped by language.  
It serves as a sandbox of experiments, exercises from courses, and other exploratory coding work.

Larger, polished projects live in their own repositories.  
This repo is intentionally broad and lightweight.

---

## Structure

Each subfolder under a language directory is a standalone mini-project.

Example structure:

    lab/
      python/
        bookbot/
        asteroids-pygame/
        ...
      typescript/
        ...
      README.md
      .gitignore

Each project folder contains its own code, and may contain a small README if needed.

---

## Projects Overview

### Python

- **bookbot** – A text analysis tool (counts, frequencies, etc.).
- **asteroids-pygame** – A simple Asteroids-style game written with Pygame.

### TypeScript

-
- 

---

## Running the Projects

### Python

Navigate into the project folder:

    cd python/<project-name>
    python3 main.py

If there's a requirements file:

    pip install -r requirements.txt

### TypeScript / Node

    cd typescript/<project-name>
    npm install
    npm run dev   (or npm start depending on project)

---

## Purpose of This Repository

This repo acts as:

- a record of learning progress,
- a central place for small projects,
- a way to keep my main GitHub profile clean and easy to read,
- a portfolio of breadth, while larger repos demonstrate depth.

---

## Internal Notes

To add a new completed project to this repo:

    cd ~/dev/lab
    git subtree add --prefix=python/<project> git@github.com:lhufdev/<project>.git main --squash

Or for TypeScript:

    git subtree add --prefix=typescript/<project> git@github.com:lhufdev/<project>.git main --squash

After importing, archive the original repo.
