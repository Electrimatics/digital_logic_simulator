# Git Workflow for Developers
This repo will follow the GitFlow Workflow with a few types of branches.

![atlassian_gitflow_diagram.png](./atlassian_gitflow_diagram.png?raw=true)

Edited from: [Atlassian Documentation on Gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

## Master
- **Description**: The production branch.
- **Naming convention**: master
- **Pull request into**: N/A
    - No one should commit directly to master.

No developer should be commiting directly to the master branch.  It will always contain the most recent "complete" version of our project.  Releases will be created off of this branch at the end of each iteration.

## Develop
- **Description**: The development branch.  This branch will contain the most up-do-date code
- **Branched from**: master
- **Naming convention**: develop
- **Pull request into**: master

No developer should be committing directly to the develo branch either.  This will be the collection of all of the features we are currently working on, and the changes in the develop branch will be pulled into master at the end of each iteration.

## Feature
- **Description**: A set of branches for each feature addition
- **Required to use**: Optional
- **Branched from**: develop
- **Naming convention**: feature/*feature-name*
- **Pull request into**: develop

These will be the collection of branches we commit our changes to.  Each new feature should have its own branch, which will typically be paired to a developer.  If two or more developers are working on one feature, it should either be broken up or additional feature branches should be branched off of the main feature branch.  When merging everything back together, ensure you merge into the branch you originally branched from.  Once the feature is complete or at the end of an iteration, the feature branches should be merged into develop.

## Examples and Commands
Example git commands are shown in the Atlassian link above.