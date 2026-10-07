# Part 4: Cloud Coding Agent (30 minutes)

## Overview
Use GitHub Copilot's cloud agent for fully autonomous development that works asynchronously.

## What is the Cloud Coding Agent?

The cloud coding agent runs completely autonomously in GitHub's infrastructure:
- Works asynchronously (you don't wait)
- Creates a new branch automatically
- Implements the feature independently
- Runs tests and fixes errors
- Opens a PR when complete

It works on the copy of the repository on GitHub, not on the files in your Codespace. For you that is your own copy of the module repo: the branch and the pull request appear there, and your `main` branch changes only if you merge the pull request.

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Chat as Copilot Chat
    participant Cloud as Cloud Agent
    participant GH as GitHub
    participant CI as CI/CD
    
    Dev->>Chat: Delegate the task to the cloud agent
    Chat->>Cloud: Trigger cloud agent
    Cloud->>GH: Create branch
    
    loop Autonomous Work
        Cloud->>Cloud: Analyze codebase
        Cloud->>Cloud: Implement changes
        Cloud->>Cloud: Run tests
        Cloud->>Cloud: Fix failures
        Cloud->>Cloud: Commit progress
    end
    
    Cloud->>GH: Push branch
    Cloud->>GH: Create PR
    GH->>CI: Run CI checks
    CI-->>GH: Report status
    GH->>Dev: Notify PR ready
    
    Dev->>GH: Review PR
    Dev->>GH: Approve & Merge
```

## Exercises

### Exercise 4.1: Trigger a Cloud Agent Task (10 min)

**Task:** Have the cloud agent implement a new feature autonomously.

**Steps:**

1. **In Copilot Chat**, press the `+` at the top of the chat panel for a fresh conversation. Open the control that says **Copilot** or **Local** (the session target) and choose **Cloud**. If **Cloud** is not in the list, choose **Copilot** and put `/delegate` and a space in front of the prompt instead. If neither starts a cloud session, the cloud agent is not available to you: skip to Part 5. Then send:

```
Create a user authentication system with:

- User registration with password hashing (bcrypt)
- Login with JWT token generation
- Password reset functionality
- Email validation
- Unit tests with >80% coverage
- README documentation

Use Flask for the web framework and SQLite for storage.

Put every file in a new folder,
lectures-and-labs/week06/agents_lab/part4_cloud_agent/auth-system/.
Do not change any file outside that folder.
```

2. **What Happens:**
   - Copilot starts a new cloud session and replies with a link to the pull request it creates
   - The agent works independently
   - You can continue other work

3. **Monitor Progress:**
   - You'll receive notifications as the agent works
   - Can check the branch being created
   - View commits in real-time

4. **Switch back:**
   - Press the `+` at the top of the chat panel and choose **Copilot** as the session again
   - VS Code remembers the session you chose last, so new conversations would otherwise start in the cloud

---

### Exercise 4.2: Review the PR (10 min)

**Task:** Review the pull request created by the agent.

**Review Checklist:**

```markdown
Files Changed:
- [ ] All required files created
- [ ] Code follows best practices
- [ ] Proper error handling
- [ ] Type hints used
- [ ] Docstrings present

Tests:
- [ ] Tests exist and pass
- [ ] Edge cases covered
- [ ] Good test coverage

Documentation:
- [ ] README updated
- [ ] Clear instructions
- [ ] Examples provided

Security:
- [ ] Passwords properly hashed
- [ ] No hardcoded secrets
- [ ] Input validation present
```

**Steps:**
1. Navigate to the PR (click notification link)
2. Review each file thoroughly
3. Run the tests locally if possible
4. Check security considerations
5. Provide feedback via comments

---

### Exercise 4.3: Iterate with the Agent (10 min)

**Task:** Request improvements to the PR.

**Steps:**

1. **In the PR comments**, tag Copilot:

```
@copilot Please add:
- Rate limiting for login attempts
- Account lockout after 5 failed attempts
- Email verification on registration
- Update tests accordingly
```

2. **Watch the Agent:**
   - It will add new commits to the PR
   - Implement the requested changes
   - Update tests
   - Push updates

3. **Final Review & Merge:**
   - Review the additional changes
   - Merge when satisfied
   - Or request more changes

---

## Cloud Agent Best Practices

### ✅ Effective Task Descriptions:

**Good ✅:**
```
Create a REST API for a library system with:
- Book CRUD operations (title, author, ISBN, status)
- Borrower management
- Checkout/return functionality
- SQLite persistence
- 80%+ test coverage
- OpenAPI documentation
```

**Too Vague ❌:**
```
Make a library app
```

### When to Use Cloud Agent:
- ✅ Large features that take >30 minutes
- ✅ When you want to work on other things
- ✅ Complete new modules
- ✅ Comprehensive test suites
- ✅ Documentation generation

### When NOT to Use:
- ❌ Quick fixes (use Edit mode)
- ❌ Learning exercises (use Ask mode)
- ❌ Experimental changes
- ❌ Critical security patches

---

## Troubleshooting

**Problem:** Cloud agent doesn't start
**Solutions:**
- Check that the session target said **Cloud**, or that the prompt began with `/delegate`, before you sent it
- Check repository permissions
- Verify Copilot subscription includes cloud features

**Problem:** PR not created
**Solutions:**
- Wait longer (can take 10-30 minutes)
- Check GitHub Actions logs
- Verify branch permissions

---

## Next Steps
When you're done with Part 4, move on to `part5_google_jules` for Google Jules!
