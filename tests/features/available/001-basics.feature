Feature: Basic Repo initialization and handling

    Scenario: Preparation
        Given I use a new temporary directory

    Scenario: First repo initialization
        Given I initialize a git repository under the temporary directory
        Given I use the repository under the temporary directory

    Scenario: First tessera initialization
        When I initialise tessera

    Scenario: Second initialization fails
        Then I initialise tessera with error

    Scenario: Add a issue
        Then I create a Tessera
