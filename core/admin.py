fromdjango.contribimportadmin

from.modelsimport(
SiteSettings,
MenuItem,
InvestmentPlan,
CryptoStat,
FeatureCard,
FeatureSection,
ProfitCalculatorSection,
ThreeStepSection,
StepItem,
Testimonial,
TeamMember,
Investor,
Transaction,
GetStartedSection,
PaymentSection,
PaymentMethod,
NewsItem,
NewsSection,
NewsCategory,
SiteFooter,
NewsTag,
NewsComment,
ContactMessage,
SiteMap,
SupportInfo,
ComplianceNotice,
SocialLink,
NewsletterSignup,
)


@admin.register(SiteSettings)
classSiteSettingsAdmin(admin.ModelAdmin):

    list_display=(
"site_name",
)

fieldsets=(
(
"General",
{
"fields":(
"site_name",
"logo",
"favicon",
)
},
),
(
"Homepage Hero",
{
"fields":(
"hero_title_white",
"hero_title_gold",
"hero_subtitle",
"hero_button_text",
"hero_background",
)
},
),
(
"About Us Section",
{
"fields":(
"about_heading",
"about_content",
"about_button_text",
"about_button_link",
)
},
),
)


@admin.register(MenuItem)
classMenuItemAdmin(admin.ModelAdmin):

    list_display=(
"title",
"url_name",
"order",
"is_active",
)

list_editable=(
"order",
"is_active",
)

search_fields=(
"title",
"url_name",
)

ordering=(
"order",
)


@admin.register(InvestmentPlan)
classInvestmentPlanAdmin(admin.ModelAdmin):

    list_display=(
"name",
"return_rate",
"frequency",
"duration",
"total_return",
"minimum_investment",
"maximum_investment",
)


@admin.register(ProfitCalculatorSection)
classProfitCalculatorSectionAdmin(admin.ModelAdmin):

    list_display=(
"heading",
"subheading",
)


@admin.register(CryptoStat)
classCryptoStatAdmin(admin.ModelAdmin):

    list_display=(
"label",
"value",
)


@admin.register(FeatureSection)
classFeatureSectionAdmin(admin.ModelAdmin):

    list_display=(
"heading",
"subheading",
)


@admin.register(FeatureCard)
classFeatureCardAdmin(admin.ModelAdmin):

    list_display=(
"title",
"is_active",
"section",
)

list_filter=(
"is_active",
"section",
)


classStepItemInline(admin.TabularInline):

    model=StepItem
extra=0


@admin.register(ThreeStepSection)
classThreeStepSectionAdmin(admin.ModelAdmin):

    list_display=(
"heading",
"subheading",
)

inlines=[
StepItemInline,
]


@admin.register(Testimonial)
classTestimonialAdmin(admin.ModelAdmin):

    list_display=(
"name",
"position",
"stars",
)


@admin.register(TeamMember)
classTeamMemberAdmin(admin.ModelAdmin):

    list_display=(
"name",
"position",
)


@admin.register(Investor)
classInvestorAdmin(admin.ModelAdmin):

    list_display=(
"name",
)


@admin.register(Transaction)
classTransactionAdmin(admin.ModelAdmin):

    list_display=(
"investor",
"transaction_type",
"direction",
"wallet",
"asset_amount",
"usd_value",
"exchange_rate",
"date",
)

list_filter=(
"transaction_type",
"direction",
"wallet__currency",
"date",
)

search_fields=(
"investor__name",
"wallet__user__username",
"reference",
"description",
)

readonly_fields=(
"date",
)


@admin.register(GetStartedSection)
classGetStartedSectionAdmin(admin.ModelAdmin):

    list_display=(
"title",
"button_text",
"button_link",
)

search_fields=(
"title",
"subtitle",
)


@admin.register(PaymentSection)
classPaymentSectionAdmin(admin.ModelAdmin):

    list_display=(
"heading",
"subheading",
)


@admin.register(PaymentMethod)
classPaymentMethodAdmin(admin.ModelAdmin):

    list_display=(
"name",
"section",
"is_active",
)

list_filter=(
"is_active",
)


@admin.register(NewsSection)
classNewsSectionAdmin(admin.ModelAdmin):

    list_display=(
"heading",
"subheading",
)


@admin.register(NewsItem)
classNewsItemAdmin(admin.ModelAdmin):

    list_display=(
"subheading",
"category",
"author",
"date",
"is_active",
)

list_filter=(
"category",
"is_active",
"date",
)

search_fields=(
"subheading",
"author",
"content_title",
)


@admin.register(SiteFooter)
classSiteFooterAdmin(admin.ModelAdmin):

    list_display=(
"company_name",
"year",
)

search_fields=(
"company_name",
)


@admin.register(NewsCategory)
classNewsCategoryAdmin(admin.ModelAdmin):

    list_display=(
"name",
"slug",
)

prepopulated_fields={
"slug":(
"name",
)
}


@admin.register(NewsTag)
classNewsTagAdmin(admin.ModelAdmin):

    list_display=(
"name",
"slug",
)

prepopulated_fields={
"slug":(
"name",
)
}


@admin.register(NewsComment)
classNewsCommentAdmin(admin.ModelAdmin):

    list_display=(
"name",
"news",
"created_at",
"approved",
)

list_filter=(
"approved",
"created_at",
)

search_fields=(
"name",
"comment",
)


@admin.register(ContactMessage)
classContactMessageAdmin(admin.ModelAdmin):

    list_display=(
"full_name",
"email",
"created_at",
)

search_fields=(
"full_name",
"email",
)


@admin.register(SiteMap)
classSiteMapAdmin(admin.ModelAdmin):

    list_display=(
"address",
)


@admin.register(SupportInfo)
classSupportInfoAdmin(admin.ModelAdmin):

    list_display=(
"type",
"heading",
"detail_line1",
"detail_line2",
)

list_filter=(
"type",
)


admin.site.register(ComplianceNotice)
admin.site.register(SocialLink)
admin.site.register(NewsletterSignup)