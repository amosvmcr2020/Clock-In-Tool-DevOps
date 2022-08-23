<script>
    import axios from "axios";

    let team_list = [];
    const get_teams = async () => {
        await axios
            .get(`http://localhost:8000/team`)
            .then((res) => (team_list = res.data));
    };
</script>

<div class="page">
    <div class="page-title">Teams</div>
    <div class="content-container">
        <div class="container-title">Teams</div>
        <div class="content">
            <button on:click={() => get_teams()}> Get Teams </button>

            {#each team_list as team}
                <div class="team-header">
                    {team.teamname}
                </div>
                <table>
                    <tr>
                        <th>Username</th>
                        <th>Role</th>
                    </tr>
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
                </table>
            {/each}
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
        display: flex;
        width: 80%;
        flex-direction: column;
        gap: 20px;
        justify-content: center;
        align-items: flex-start;
    }

    td {
        padding-left: 60px;
    }
    th {
        padding-left: 30px;
    }
</style>
