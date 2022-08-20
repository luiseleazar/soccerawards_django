import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Functions used for tests
def create_question(question_text, days):
    """Create a question with given question_text and 
    published the given number of days offset to now"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


# Tests
class QuestionCreationTests(TestCase):
    # TODO: Modify Question Models in order that object can't be instanced
    # if doesn't have at least one choice

    # TODO: Create a test that evaluates the above problem
    pass


class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_question(self):
        """was_published_recently returns False
        for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_past_question(self):
        """was_published_recently returns False
        for questions whose pub_date is more than 30 days in the past"""
        time = timezone.now() - datetime.timedelta(days=1, minutes=1)
        future_question = Question(question_text="", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_present_question(self):
        """was_published_recently returns True
        for questions whose pub_date is the present time"""
        time = timezone.now()
        future_question = Question(question_text="", pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)
    
    def test_was_published_recently_with_almost_24_hours_question(self):
        """was_published_recently returns True
        for questions whose pub_date is less than 23 hrs 59 minutes"""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59)
        future_question = Question(question_text="", pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):

    def test_no_question(self):
        """If no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question(self):
        """Question with future pub_date are not displayed
        on index page"""
        create_question("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_questiion(self):
        """Question with past pub_date are displayed
        on index page"""
        question = create_question("Past question", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_future_question_and_past_question(self):
        """Even if both past and future exist,
        only past question is displayed"""
        past_question = create_question(question_text="Past question", days=-30)
        future_question = create_question(question_text="Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )

    def test_two_past_question(self):
        """The question index page may displayed multiple questions"""
        past_question1 = create_question(question_text="Past question 1", days=-30)
        past_question2 = create_question(question_text="Past question 2", days=-40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1, past_question2]
        )

    def test_two_future_question(self):
        """The question index page may displayed multiple questions"""
        future_question1 = create_question(question_text="Future question 1", days=30)
        future_question2 = create_question(question_text="Future question 2", days=40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            []
        )


class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """The detail view of a question with a future pub_date
        returns 404 Error Not Found"""
        future_question = create_question(question_text="Future question", days=30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_past_question(self):
        """The detail view of a question with a past pub_date
        displays the question's text"""
        past_question = create_question(question_text="Past question", days=-30)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResultsViewTests(TestCase):
    # TODO: create tests for results view
    pass