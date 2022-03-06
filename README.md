# Rao Academy

Rao Academy has been designed to serve as a one stop online learning platform, aimed at providing all learning enthusiasts with quality online education, free of cost. 

As mentioned above, this project is an online learning platform, where educationists/institutions can create courses, and build structured notes (content) for those courses. They also have the ability to edit/delete any course or any note which they have created. 

The learning platform offers other features such as users can also ‘subscribe’ to the courses they want to learn and can also ‘follow’ professors. Apart from this, users have the option to  ‘like’ the notes and post comments on each note without having to reload the page. The Search option provides users to perform a thorough search of all the courses on the website and displays a list of courses that are related to the search query.


### Features of the project

1. **Course Card** - Each course card displays the course thumbnail, title and description. If the title has over 50 characters, then only the first 50 characters of the title are displayed with a ‘...’ at the end. Similarly, if the description has over 100 characters, only the first 100 characters are displayed with a ‘...’ at the end. Clicking on the course card will take you to that particular course’s page.

2. **Note Card** -  Each note card displays a thumbnail, title, and description. If the note has a thumbnail then that is displayed, else if the note doesn’t have a thumbnail then the course thumbnail is displayed. If the title has over 50 characters, then only the first 50 characters of the title are displayed with a ‘...’ at the end. Similarly, if the description has over 100 characters, only the first 100 characters are displayed with a ‘...’ at the end. Clicking on the note card will take you to that particular notes page. 

3. **Create Course** - While creating a course, the category field is optional and the options in the category field have been sorted in alphabetical order. A user cannot have two or more courses with the same name, hence a warning message will be displayed if the user tries to do so. A user who doesn’t have the lecturer value as true will not be allowed to create a course.

4. **Upload Notes** - While creating notes, the thumbnail field, video iframe field, additional tags field are optional. The options in the courses field have been filtered in such a way that only those courses are shown that have been created by the user who is trying to create the note. A user who doesn’t have the lecturer value as true will not be allowed to upload a note. The content of the note must be in markdown!

5. **Paginator** - Index Page, Category View Page, Subscribed Courses Page, and the Following Lecturers’ Courses Page has the paginator (only 9 courses are displayed per page).

6. **Course View** - The course view contains some course details, and also a list of all the notes that are present in that particular course. This page also contains the subscribe button for everyone except the course creator. This page provides the edit course and the delete course buttons which are only visible to the course creator. 

7. **Subscribe Course** - All authenticated users except the course creator can subscribe and unsubscribe to a course. This is achieved without having to reload the page.

8. **Edit Course** - Editing a course can be done without reloading the page. When all other fields except the course name have been changed, then the respective elements on the page are updated with the new content. The course view URL is of the format:  ```/<lecturer>/<course name>```, therefore if the title has been changed, the URL will also change. Hence, in spite of the title being changed without reloading the page, the user is still redirected to a new page that contains the edited title and URL. Since a user cannot have more than one course with the same name, the user will be warned if he/she tries to do the same.

9. **Delete Course** - When the 'Delete Course' button is clicked, the user is prompted with a message to confirm if he/she is sure about deleting the course. This message will also mention all the notes that will be deleted if the course is deleted. Upon clicking 'Delete' again, the course along with all the notes in this course will be deleted.

10. **Note View** - The Note View contains some note details, the video iframe (if any), the markdown content converted to HTML, the thumbnail, etc. Besides, this page also contains a 'Like' button for everyone except the course creator. The 'Edit Note' and 'Delete Note' buttons are only visible to the note creator. Additionally, at the bottom of the page any user who is authenticated will have access to post comments. 

11. **Like Note** - All authenticated users except the course creator can ‘like’ and ‘unlike’ a note. This is achieved without having to reload the page.

12. **Edit Note** - Editing a note can be done without reloading the page. Again, here also, only the courses created by the user will be displayed in the Courses field. If the notes content has been changed, a JS library has been used to convert it from markdown to HTML.

13. **Delete Note** - When the 'Delete Note' button is clicked, the user will be once again asked to confirm if he/she is sure about deleting the note. Upon clicking ‘Delete’ again, the note will be deleted.

14. **Comments** - Any user who is authenticated can post a comment. The comment will be added to the page without reloading the site. Since a note may have many comments, the **infinite scroll** concept has been implemented. So every time a user scrolls to the bottom of the page, a new set of comments loads.

15. **Category Page** - This page displays all the courses associated with that particular category. For example, even if some courses don’t have categories assigned to them, but the notes in the course may have that particular category, then the course will still be displayed.

16. **Search** - Whenever a user searches for something, the search results are based on the category names, course names, notes’ names, additional category/tags of the notes, or even the lecturers’ names.

17. **Profile View** - This page displays:
    - The number of followers the profile person (Lecturer) has
    - The total number of subscribers this profile person’s courses have
    - The total number of likes this profile person’s notes have
    - A list of the courses created by this profile person
    For everyone except the profile person, a follow/unfollow button will also be visible. If a user’s page is visited who is not a lecturer, then a message will be displayed stating that the user is not a lecturer.

18. **Follow/Unfollow** - All authenticated users except the profile person (lecturer) have the option to ‘follow’ or ‘unfollow’ the lecturer. This is achieved without having to reload the page. Users can only follow and unfollow lecturers, they cannot follow/unfollow other users who are not lecturers.

19. **Following Lecturers’ Courses** - This page contains all the lecturers’ courses the user is following.

20. **Subscribed Courses** - This page contains all the courses the user has subscribed to. The order of the courses is as per the most recent courses the user has subscribed.

21. **Mobile Responsive** - This website is completely mobile responsive.


### Each file’s content

1. categories.html - Contains a list of all the categories sorted alphabetically.
2. category.html -  Contains a list of courses associated with that particular category.
3. course_view.html - Contains a list of notes that are part of the course along with course details, subscribe, edit, and delete buttons.
4. create_course.html - Contains a form to create a course.
5. following_lecturer_courses.html - Contains a list of courses of the lecturers the user is following.
6. index.html - Contains a list of all the courses.
7. layout.html - Contains the navigation bar and some meta tags.
8. login.html - Contains a form for users to log in.
9. note_view.html - Contains the note details, content, video iframe, like, edit, delete buttons. This file also contains the comments and the form to post the comments.
10. profile_view.html - contains a list of courses created by that profile along with a follow button.
11. register.html - Contains a form for people to register and make an account.
12. search.html - Contains a list of courses related to the search entry.
13. subscribed_course.html - Contains a list of courses that the user has subscribed to.
14. upload_notes.html - Contains a form to create a note.
15. styles.css - Contains the styling for the website.
16. views.py - Contains all the views for the website.
17. urls.py - Contains all the URLs for the website.
18. models.py - Contains all the models for the website.


### How to run the project

1. In your terminal ```cd``` into directory
2. Run ```python manage.py makemigrations online_edu``` to make migrations for the online_edu app.
3. Run ```python manage.py migrate``` to apply migrations to your database.
4. Run ```python manage.py runserver``` to run the server.

### Important: 
- If you create a superuser, then please be sure to create a profile for this superuser account on the django admin page.
- On the django admin page, in the User model, please make the lecturer boolean value to true, only then can a user create courses and notes.


