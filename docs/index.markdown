---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---
**Welcome to the Connect-4 Website!**

Be sure to check out our documentation, or feel free to check our our group members!
  


  

This Feed Contains all of our deliverables

<ul>
    {% for post in site.posts %}
        <li>
            <a href="{{ post.url }}">{{ post.title }}</a>
        </li>
    {% endfor %}
</ul>