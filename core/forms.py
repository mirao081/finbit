fromdjangoimportforms
from.modelsimportNewsComment,ContactMessage,NewsletterSignup


classNewsCommentForm(forms.ModelForm):

    classMeta:
        model=NewsComment

fields=[
"name",
"email",
"image",
"comment",
]

widgets={
"name":forms.TextInput(attrs={
"placeholder":"Your Name",
"class":"ndxv9-input"
}),

"email":forms.EmailInput(attrs={
"placeholder":"Email Address",
"class":"ndxv9-input"
}),

"image":forms.ClearableFileInput(attrs={
"class":"ndxv9-input",
"accept":"image/*"
}),

"comment":forms.Textarea(attrs={
"placeholder":"Write your comment...",
"class":"ndxv9-textarea"
})
}

classContactMessageForm(forms.ModelForm):
    classMeta:
        model=ContactMessage
fields=["full_name","email","message"]
widgets={
"full_name":forms.TextInput(attrs={
"placeholder":"Full Name",
"class":"form-input"
}),
"email":forms.EmailInput(attrs={
"placeholder":"Email Address",
"class":"form-input"
}),
"message":forms.Textarea(attrs={
"placeholder":"Message",
"rows":5,
"class":"form-input"
}),
}

classNewsletterSignupForm(forms.ModelForm):
    classMeta:
        model=NewsletterSignup
fields=["email"]
widgets={
"email":forms.EmailInput(attrs={
"placeholder":"Enter your email",
"class":"newsletter-input"
})
}