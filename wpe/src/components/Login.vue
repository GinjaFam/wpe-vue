<template>
    <div class="modal fade" id="loginModal" tabindex="-1" aria-labelledby="loginModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="loginModalLabel">Login</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <!-- Login form here -->
                    <!-- <form id="login-form" action="/login" method="POST" autocomplete="off">
                        
                        
                        <input type="hidden" name="form_type" value="login">
            
                        {{log_form.hidden_tag()}}
            
                        {{log_form.email.label(class='form-label')}}
                        {{log_form.email(class='form-control')}}
            
                        {{log_form.password.label(class='form-label')}}
                        {{log_form.password(class='form-control')}}
                        
                        <br/>
                        
                        {{log_form.submit(class='btn-light')}} -->
            
                    <!-- </form> -->
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'Login'
    }
</script>