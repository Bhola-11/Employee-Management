import os

def w(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f'Wrote: {path}')

w ('templates/dashboard/search_results.html', '''{% extends 'base/base.html' %}
{% block title %}Search Results for "{{ query }}"{%{ endblock %}
{% block content %}
<div class="page-header">
  <div>
    <h1 class="page-title">Search Results</h1>
    <div class="breadcrumbs">Query: "<strong>{{ query }}</strong>"</div>
  </div>
</div>
<div class="card">
  <div class="card-header"><span><i class="fa-solid fa-users me-2 text-primary"></i> Matching Employees</span></div>
  <div class="card-body" style="padding: 0;">
    <table class="table">
      <thead><tr><th>Name</th><th>Employee ID</th><th>Designation</th><th>Department</th></tr></thead>
      <tbody>
        {% for emp in results.employees %}
        <tr>
          <td><a href="{% url 'employees:detail' emp.id %}" style="font-weight: 600;">{{ emp.name }}</a></td>
          <td><code>{{ emp.employee_id }}</code></td>
          <td>{{ emp.designation }}</td>
          <td>{{ emp.department }}</td>
        </tr>
        {% empty %}
        <tr><td colspan="4" style="text-align: center; color: #64748b; padding: 1.5rem;">No matching employee records.</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}
''')

w ('templates/accounts/login.html', '''{% extends 'base/base.html' %}
{% block title %}Sign In{% endblock %}
{% block auth_content %}
<div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; background: radial-gradient(circle at 10% 20%, #1e293b 0%, #0f172a 90%); padding: 1.5rem;">
  <div style="width: 100%; max-width: 440px; background: #ffffff; border-radius: 12px; padding: 2.25rem; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);">
    <div style="text-align: center; margin-bottom: 2rem;">
      <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #2563eb, #3b82f6); border-radius: 10px; display: inline-flex; align-items: center; justify-content: center; color: #fff; font-size: 1.5rem; margin-bottom: 0.75rem;">
        <i class="fa-solid fa-cube"></i>
      </div>
      <h2 style="font-size: 1.5rem; font-weight: 700; color: #0f172a;">WorkSphere GENT</h2>
      <p style="color: #64748b; font-size: 0.875rem; margin-top: 0.25rem;">One Platform for Every Workforce</p>
    </div>

    <form method="post" action="{% url 'accounts:login' %}">
      {% csrf_token %}
      {% if form.non_field_errors %}
      <div style="background-color: #fee2e2; color: #991b1b; padding: 0.75rem; border-radius: 6px; font-size: 0.85rem; margin-bottom: 1rem;">
        {{ form.non_field_errors }}
      </div>
      {% endif %}

      <div class="form-group">
        <label class="form-label" style="color: #1e293b;">Work Email</label>
        {{ form.email }}
      </div>

      <div class="form-group">
        <label class="form-label" style="color: #1e293b;">Password</label>
        {{ form.password }}
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; font-size: 0.85rem;">
        <label style="display: flex; align-items: center; gap: 0.5rem; color: #475569;">
          {{ form.remember_me }} Remember this device
        </label>
      </div>

      <button type="submit" class="btn btn-primary" style="width: 100%; justify-content: center; padding: 0.65rem;">
        <i class="fa-solid fa-lock"></i> Sign In to WorkSphere
      </button>
    </form>

    <div style="margin-top: 1.75rem; padding-top: 1.25rem; border-top: 1px solid #e2e8f0; font-size: 0.775rem; color: #64748b; text-align: center;">
      Protected by Enterprise RBAC & Comprehensive Audit Logging.<br>
      WorkSphere Platform v1.0.0-Enterprise
    </div>
  </div>
</div>
{% endblock %}
''')

w ('templates/accounts/profile.html', '''{% extends 'base/base.html' %}
{% block title %}My Account & Security{% endblock %}
{% block content %}
<div class="page-header">
  <div>
    <h1 class="page-title">User Profile & Security Settings</h1>
    <div class="breadcrumbs">Manage your personal account settings, theme preferences, and active role assignments.</div>
  </div>
</div>
<div class="grid-2">
  <div class="card">
    <div class="card-header"><span><i class="fa-solid fa-user-gear me-2 text-primary"></i> Account Details</span></div>
    <div class="card-body">
      <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <div class="form-group"><label class="form-label">First Name</label>{{ form.first_name }}</div>
        <div class="form-group"><label class="form-label">Last Name</label>{{ form.last_name }}</div>
        <div class="form-group"><label class="form-label">Phone</label>{{ form.phone }}</div>
        <div class="form-group"><label class="form-label">Profile Avatar</label>{{ form.avatar }}</div>
        <div class="form-group"><label class="form-label">Preferred Language</label>{{ form.preferred_language }}</div>
        <button type="submit" class="btn btn-primary"><i class="fa-solid fa-check"></i> Save Profile</button>
      </form>
    </div>
  </div>
  <div>
    <div class="card">
      <div class="card-header"><span><i class="fa-solid fa-id-card-clip me-2 text-primary"></i> Assigned Roles</span></div>
      <div class="card-body">
        {% for a in roles %}
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.65rem 0; border-bottom: 1px solid #e2e8f0;">
          <div>
            <strong>{{ a.role.name }}</strong> (<code>{{ a.role.code }}</code>)
            <div style="font-size: 0.75rem; color: #64748b;">Organization: {{ a.organization.name }}</div>
          </div>
          {% if a.is_primary %}<span class="badge badge-primary">Primary Role</span>{%{ endif %}
        </div>
        {% empty %}
        <p style="color: #64748b;">Super Admin account</p>
        {% endfor %}
      </div>
    </div>
    <div class="card">
      <div class="card-header"><span><i class="fa-solid fa-clock me-2 text-primary"></i> Recent Login Sessions</span></div>
      <div class="card-body" style="padding: 0;">
        <table class="table">
          <thead><tr><th>IP Address</th><th>Login Time</th><th>Status</th></tr></thead>
          <tbody>
            {% for s in sessions %}
            <tr>
              <td><code>{{ s.ip_address }}</code></td>
              <td>{{ s.login_time|date:'M d, Y H:i' }}</td>
              <td>{u if s.is_active %}<span class="badge badge-success">Active</span>{%{ else %}<span class="badge badge-secondary">Closed</span>{%{ endif %}</td>
            </tr>
            {% empty %}
            <tr><td colspan="3" style="text-align: center; color: #64748b;">No past sessions found.</td></tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
{% endblock %}
''')
