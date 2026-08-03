# First Technical Milestone

This is where we begin.

## Sprint 0

Create:
```
Repository
Folder Structure
Git Repository
requirements.txt
README.md
```

Install only:
```
faker
requests
sqlite3
pytest
```

(We'll keep dependencies intentionally small.)

## Sprint 0 Success Criteria

You should end Sprint 0 with:

✅ Local Git repository

✅ Final folder structure

✅ requirements.txt

✅ Initial README

✅ Empty SQLite file
```
warehouse.db
```

✅ Project can be run from:
```
python main.py
```

even if it only prints:
```
Synthetic E-Commerce Analytics Platform
```
# Coaching Note

The most important decision you made in the charter was the move toward session-driven event data.

That single decision will let you learn:

* Event modeling
* ELT architecture
* SQL transformations
* Analytics engineering
* Customer journey analysis
* Incremental processing

all within one project.

That is significantly richer than a simple "orders and products" pipeline.

For now, treat Sprint 0 as your only target. Don't think about Silver, Gold, or the orchestrator yet. A common junior-engineer mistake is to design ten steps ahead before the first directory exists.

Let's win Sprint 0 first, then we'll design Phase 1 like a real engineering team.