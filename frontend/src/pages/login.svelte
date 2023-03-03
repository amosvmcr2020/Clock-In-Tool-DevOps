<script>
    import axios from "axios";
    import { current_user_id } from "../store";
    import { useNavigate, useLocation } from "svelte-navigator";

    export let alerts = [];

    const navigate = useNavigate();
    const location = useLocation();

    let login = true;
    let team_list = [];

    const toggleLogin = async () => {
        login = !login;
    };

    const get_teams = async () => {
        await axios
            .get(`http://0.0.0.0:8000/team`)
            .then((res) => (team_list = res.data));
        team_list = team_list;
    };
    get_teams();

    const onSubmit = async (e) => {
        const formData = new FormData(e.target);

        const data = {};
        for (let field of formData) {
            const [key, value] = field;
            data[key] = value;
        }
        if (login) {
            try {
                await axios
                    .post(`http://0.0.0.0:8000/login`, {
                        username: data.username,
                        password: data.password,
                    })
                    .then((res) =>
                        current_user_id.update((val) => (val = res.data))
                    );
                alerts = alerts;
                navigate("/home", {
                    state: { from: $location.pathname },
                    replace: true,
                });
            } catch (error) {
                alerts.push(["Error", error.response.data.detail]);
                alerts = alerts;
            }
        } else {
            try {
                await axios
                    .post(`http://0.0.0.0:8000/user`, {
                        username: data.username,
                        password: data.password,
                        teamID: data.teamID,
                        hasAdmin: data.hasAdmin,
                    })
                    .then((res) =>
                        current_user_id.update((val) => (val = res.data.id))
                    );
                navigate("/home", {
                    state: { from: $location.pathname },
                    replace: true,
                });
            } catch (error) {
                alerts.push(["Error", error.response.data.detail]);
                alerts = alerts;
            }
        }
    };
</script>

<div class="page">
    {#if login}
        <div class="page-title">Login</div>
        <div class="">
            <form
                autocomplete="off"
                class="modalForm"
                on:submit|preventDefault={onSubmit}
            >
                <label for="username">Username</label>
                <input type="text" name="username" placeholder="Username" />

                <label for="password">Password</label>
                <input type="password" name="password" placeholder="Password" />
                <input class="end" type="submit" value="Submit" />
            </form>
            <br />
            <div class="content bottom">
                Want to create a new user?
                <button on:click={() => toggleLogin()}> Create User</button>
            </div>
        </div>
    {:else}
        <div class="page-title">Create User</div>
        <div class="">
            <form
                autocomplete="off"
                class="modalForm"
                on:submit|preventDefault={onSubmit}
            >
                <label for="username">Username</label>
                <input type="text" name="username" placeholder="Username" />
                <label for="username">Password</label>
                <input type="password" name="password" placeholder="Password" />

                <label for="hasAdmin">Admin? </label>
                <select name="hasAdmin" id="hasAdmin">
                    <option value="true">true</option>
                    <option selected="selected" value="false"> false </option>
                </select>

                <label for="teamname">Team Name</label>
                <select name="teamID" id="teamname">
                    {#each team_list as team}
                        <option value={team.id}>{team.teamname}</option>
                    {/each}
                </select>

                <input class="end" type="submit" value="Submit" />
            </form>
            <br />
            <div class="content bottom">
                Already have an account?
                <button on:click={() => toggleLogin()}> Log In</button>
            </div>
        </div>
    {/if}
</div>

<style>
    form {
        color: var(--text);
    }
</style>
