<script>
    import { current_user_id } from "../store";
    import { useNavigate, useLocation } from "svelte-navigator";

    const navigate = useNavigate();
    const location = useLocation();

    $: if (!$current_user_id) {
        navigate("/login", {
            state: { from: $location.pathname },
            replace: true,
        });
    }
</script>

{#if $current_user_id}
    <slot />
{/if}
