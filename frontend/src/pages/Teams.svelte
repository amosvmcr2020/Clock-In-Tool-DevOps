<script>
    import axios from "axios";

    let team_list = [];
    const get_teams = async () => {
        await axios
            .get(`http://localhost:8000/team`)
            .then((res) => (team_list = res.data));
        return team_list;
    };
</script>

<div class="page">
    <div class="page-title">Teams</div>
    <div class="content-container">
        <div class="container-title">Teams</div>
        <div class="content">
            {#await get_teams()}
                Loading...
            {:then team_list}
                {#each team_list as team}
                    <div class="team-header">
                        {team.teamname}
                    </div>
                    <table>
                        <tr>
                            <th>Username</th>
                            <th>Role</th>
                        </tr>
                        <tbody>
                            {#each team.users as user}
                                <tr>
                                    <td>
                                        {user.username}
                                    </td>
                                    <td>
                                        {#if user.hasAdmin}
                                            Admin
                                        {:else}
                                            User
                                        {/if}
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                {/each}
            {/await}
        </div>
    </div>
</div>

<style>
    .team-header {
        margin: 20px;
        color: var(--text);
        text-transform: capitalize;
        font-size: 32px;
        font-weight: 100;
    }

    table {
        text-align: center;
    }
</style>
