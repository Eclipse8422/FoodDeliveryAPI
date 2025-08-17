from django.contrib import admin
from .models import DeliveryAgent

@admin.register(DeliveryAgent)
class DeliveryAgentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'pincode', 'is_available', 'is_approved', 'created_at')
    list_filter = ('is_available', 'is_approved', 'pincode')
    search_fields = ('user__email', 'user__username', 'pincode')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_selected_agents']

    def approve_selected_agents(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} delivery agent(s) approved.")
    approve_selected_agents.short_description = "Approve selected delivery agents"
