<script>
    import { Link } from "svelte-navigator";
    import { get } from "svelte/store";
    import { current_user_id } from "../store";

    const logout = () => {
        current_user_id.update((val) => (val = 0));
        console.log(get(current_user_id));
    };
</script>

<div class="topBar">
    <div class="title">Clock In Tool</div>
    <Link to="/">Home</Link>
    <Link to="/user">User</Link>
    <Link to="/clocks">Clock-In</Link>
    <Link to="/team">Teams</Link>
    <button class="logoutButton" on:click={() => logout()}> Log Out</button>
</div>

<style>
    .topBar {
        width: 100%;
        height: 80px;
        position: fixed;
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
