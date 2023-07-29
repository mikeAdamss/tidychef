Yeah it's a odd one, let me try and explain my thinking.

So as I understand it, Andrews created an architectural pattern where he's github as a bucket for data submissions to trigger github actions to publish csvw to github pages and Jenkins to load them into PMD.

Do I like that? No, I'd prefer to use buckets as buckets and handle the rest in a more typical way (to his credit though, he's made a working thing with very little development resource, I can see where he was coming from).

But.. given that's where we're at, I can only really see a few obvious options:

- (a) Allow it and try and make it sensible.
- (b) Make his team (or the DEs) review/approve data prs.
- (c) Add the external people as collaborators on an as needed basis.
- (d) Develop a different system for partner data submissions.

I was assuming (a) which is why I started talking about shunting the more security conscious things to ONSDigital (and because they probably should be on ONSDigital and because he's a grade 7 and I'm expecting Eleanor to say c+d). 