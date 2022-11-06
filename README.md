# Ideas
#### Video Demo:https://www.youtube.com/watch?v=Ijv9RYmxCBU&ab_channel=AoibheannFegan
### Description
Ideas is a web application which allows users to submit ideas to their company and other users/company employee's to vote on submitted ideas. The purpose of this is to create a more collaborative working enviornment and give employees a sense of ownership in the direction of the company.

First, companies and users within those companies will need to register for an account. If a user who's company has not yet been registered tries to register, they will be asked to register their company first. When a user registers their company they will also register themselves as a user. By default, the user who registers the company has admin permissions. Any additional users who register are registered with 'user' permissions. When a user registers all the fields must be filled and valid input entered or they will recieve an error. Once registered you will automatically be signed in. If a user has already registered they can login.

When signed in,users will be taken to the homepage which contains a Kanban style view of all the current ideas that have been submitted, under their current funnel. Their are four idea funnels - submitted, in review, accepted, rejected. There is also a link at the bottom of the page for the user to submit their own idea.

If a user navigates to the vote page they will see a summary of the current idea submissions and will be able to vote on them. An idea cannot be voted on if it has been moved out of the submission funnel. Each user can only upvote or downvote an idea once and cannot vote on their own ideas. If an idea reaches a certain number of upvotes then the idea moves to 'In Review', if the idea receives a certain number of downvotes it is automatically rejected.

If the user navigates to the ideas page they will see a table of all the current ideas along with their stage and number of upvotes or down votes received. Their is an option to filter to filter by stage.

If the user navigates to history they will see a table of any actions they have taken on ideas - submitted, upvoted or downvoted and a timestamp.

If the user navigates to 'submit idea' they will have the option to submit an idea. An idea should contain a title and a description. If neither of these are included or if the title has already been used then the user will receive an error.

From the homepage, vote or idea pages the user can click on the idea title and see a summary page of the idea. On this page, all users have the option to leave comments on an idea. The only comments visible will be the comments relevant to that idea. If the idea is at the submission stage, users will also see an option to upvote or downvote an idea here. If the idea is 'in review' then 'admin' users will have the option to accept or reject an idea.

The settings page allows admins to update existing company users' permissions. If you are not an admin the settings page will not be visible.