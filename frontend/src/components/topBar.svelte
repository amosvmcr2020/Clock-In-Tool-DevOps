<script>
    import { Link } from "svelte-navigator";
    import { current_user_id } from "../store";
    import axios from "axios";
    import AdminBar from "./adminBar.svelte";

    const logout = () => {
        $current_user_id = null;
        // current_user_id.update((val) => (val = 0));
        // window.location.reload();
    };

    const check_admin = async (userID) => {
        let hasAdmin = false;
        if (userID == null) {
            return false;
        }
        await axios
            .get(`http://localhost:8000/user/${userID}`)
            .then((res) => (hasAdmin = res.data.hasAdmin));
        return hasAdmin;
    };
</script>

<div class="container">
    {#await check_admin($current_user_id) then hasAdmin}
        {#if hasAdmin}
            <AdminBar />
        {/if}
    {/await}
    <div class="topBar">
        <div class="title">Clock In Tool</div>
        <Link to="/home">Home</Link>
        <Link to="/user">User</Link>
        <Link to="/team">Teams</Link>
        {#if $current_user_id}
            <button class="logoutButton" on:click={() => logout()}>
                Log Out</button
            >
        {/if}
    </div>
</div>

<style>
    .container {
        position: fixed;
        width: 100%;
        height: 80px;
    }
    .topBar {
        /* background: linear-gradient(90deg, var(--primary) 10%, var(--secondary) 100%); */
        background-color: var(--secondary);
        color: var(--text);
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;

        box-shadow: 0.1px 0.1px 0.1px 1px #ffffff;

        z-index: 2;

        display: flex;
        align-items: center;
        justify-content: left;
        border-radius: 0 0 1% 1%;
        flex-direction: row;
        gap: 40px;
    }

    .title {
        font-size: 32px;
        padding: 20px;
        text-transform: uppercase;
    }

    .logoutButton {
        background-color: var(--primary);
        color: var(--text);
    }
    .logoutButton:hover {
        background-color: var(--alt-primary);
    }
</style>
