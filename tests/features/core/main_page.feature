@main_page
Feature: Simple tests for demonstration

  Background:
    Given User goes to avsw.ru page

  @dev_regression @test_example
  Scenario: User opens avsw.ru and wait
    Then User is on avsw.ru page
    Then Wait for 10 seconds

  @dev_regression @see_cookie_warning
  Scenario: User is able to see cookie warning
    Then User is on avsw.ru page
    Then User see text: We use cookies. This allows us to analyze how visitors interact with the site and make it better. By continuing to use the site, you agree to  in body
    Then User see text: the terms of use in body
    Then User see text:  of cookies. in body

  @dev_regression @read_more
  Scenario: User is able to go to Read more page
    Then User is on avsw.ru page
    When User clicks Read more element
    Then User is on avsw.ru/products/anti-apt/athena page
