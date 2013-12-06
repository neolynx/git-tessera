Feature: Basic Repo initialization and handling

    Scenario: First repo initialization
        Given I initialize a git repository under "/tmp/testrepo/"
        Given I use the repository under "/tmp/testrepo"

    Scenario: First tessera initialization
        When I initialise tessera

    Scenario: Second initialization fails
        Then I initialise tessera with error

    Scenario: Add a issue
        Then I create a Tessera
