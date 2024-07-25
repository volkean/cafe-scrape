window.addEventListener("DOMContentLoaded", function() {
  document.getElementById('form1').addEventListener("submit", function(e) {
    e.preventDefault(); // before the code

    document.getElementById('error_message').innerHTML = "";
    document.getElementById('info_message').innerHTML = "";

    e.target.submit();// Will be triggered on form submit

    // Disable each input
    const inputs = document.querySelectorAll('form input');
    inputs.forEach(input => {
        input.disabled = true;
    });
  })
});