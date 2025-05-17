<script lang="ts">
    // Import any necessary stores or components for a real dashboard
</script>

<div class="p-6 md:p-10">
    <h1 class="text-3xl font-bold text-gray-800 mb-6">Welcome to The Planner's Assistant</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-white p-6 rounded-lg shadow">
            <h2 class="text-xl font-semibold text-gray-700 mb-3">Development Management</h2>
            <p class="text-gray-600 mb-4">Manage development applications effectively.</p>
            <a href="/dev-management/assessment" 
               class="inline-block bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition-colors">
                New Application / View Applications
            </a>
            <div class="mt-4">
                <h3 class="text-lg font-medium text-gray-700 mb-2">Recent Applications</h3>
                <ul class="space-y-1 text-sm text-gray-600">
                    <li>APP-001 - 123 Main St - In Progress</li>
                    <li>APP-002 - 466 Elm St - Approved</li>
                </ul>
            </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow">
            <h2 class="text-xl font-semibold text-gray-700 mb-3">Plan Production</h2>
            <p class="text-gray-600 mb-4">Drive forward local plan production.</p>
            <div class="flex space-x-3 mb-4">
                 <a href="/plan-making/policy" class="flex-1 text-center bg-blue-500 text-white p-3 rounded hover:bg-blue-600 transition-colors">Policy Tools</a>
                <a href="/plan-making/site-allocation" class="flex-1 text-center bg-blue-500 text-white p-3 rounded hover:bg-blue-600 transition-colors">Site Tools</a>
                <a href="/plan-making/scenario" class="flex-1 text-center bg-blue-500 text-white p-3 rounded hover:bg-blue-600 transition-colors">Scenario Tools</a>
            </div>
            <div>
                <h3 class="text-lg font-medium text-gray-700 mb-2">Current Projects</h3>
                 <ul class="space-y-1 text-sm text-gray-600">
                    <li>Housing Strategy Update</li>
                    <li>Retail Impact Assessment</li>
                </ul>
            </div>
        </div>
    </div>
</div>