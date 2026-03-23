def render_admin_dashboard(stats, recent_users):
    # This shell uses script.css for styling
    return f"""
    <html>
    <head>
        <link rel="stylesheet" href="/css/script.css">
    </head>
    <body class="admin-body">
        <div class="sidebar">
            <div class="sidebar-hdr">ATLAS ADMIN</div>
            <div class="sidebar-nav">
                <a href="#" class="nav-item active">Dashboard</a>
                <a href="#" class="nav-item">Manage Spots</a>
                <a href="#" class="nav-item">Tourists</a>
                <a href="#" class="nav-item">Settings</a>
            </div>
        </div>

        <div class="main-content">
            <h1 style="margin-bottom: 24px;">System Overview</h1>

            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-val">{stats['total_tourists']}</span>
                    <span class="stat-lbl">Total Tourists</span>
                </div>
                <div class="stat-card">
                    <span class="stat-val">{stats['total_spots']}</span>
                    <span class="stat-lbl">Active Spots</span>
                </div>
                </div>

            <div class="admin-table-wrap">
                <table class="admin-table" width="100%">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join([f'''
                        <tr>
                            <td>{u['fname']} {u['lname']}</td>
                            <td>{u['email']}</td>
                            <td><span class="status-pill status-{u['status']}">{u['status']}</span></td>
                            <td><button class="action-btn">Edit</button></td>
                        </tr>
                        ''' for u in recent_users])}
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """