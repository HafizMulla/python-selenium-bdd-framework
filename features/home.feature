@smokes
Feature: Homepage -  General

    Scenario: Homepage loads and displays correctly
        Given The browser is launched
        When I have navigated to the "/" page
        Then The page has loaded
        Then It should accept the cookies if available
        And The page should display with no errors
        And The main menu should display
        And The search block should display
        And The main content should display
        And destination map should display
        And the footer should display
