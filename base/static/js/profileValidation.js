//basic
// label para e-mail input
var hint_email = document.getElementById("hint_id_email");
hint_email.innerHTML = "Enter a valid e-mail: your@mail.com";

// handlers functions
function alertNameInput() {
  var socialName = document.getElementById("id_social_name");
  var invalidName = document.createElement("p");
  invalidName.classList.add("invalid-feedback");
  var invalidText = document.createTextNode(
    "Por favor, escreva como gostaria de ser chamado."
  );
  invalidName.appendChild(invalidText);
  socialName.parentElement.appendChild(invalidName);
  socialName.classList.add("is-invalid");
  socialName.focus();
}

function alertEmailInput() {
  var email = document.getElementById("id_email");
  var invalidEmail = document.createElement("p");
  invalidEmail.classList.add("invalid-feedback");
  var invalidText = document.createTextNode(
    "Por favor, indique um e-mail válido"
  );
  invalidEmail.appendChild(invalidText);
  email.parentElement.appendChild(invalidEmail);
  email.classList.add("is-invalid");
  email.focus();
}

function alertPhoneInput(id) {
  var phone = document.getElementById(id);
  var invalidPhone = document.createElement("p");
  invalidPhone.classList.add("invalid-feedback");
  var invalidText = document.createTextNode(
    "Por favor, cadastre um número de telefone válido!"
  );
  invalidPhone.appendChild(invalidText);
  phone.parentElement.appendChild(invalidPhone);
  phone.classList.add("is-invalid");
  phone.focus();
}

function alertSOSContactInput() {
  var contact_sos = document.getElementById("id_sos_contact");
  var invalidContact = document.createElement("p");
  invalidContact.classList.add("invalid-feedback");
  var invalidText = document.createTextNode(
    "Qual o nome do seu contato de emergência?"
  );
  invalidContact.appendChild(invalidText);
  contact_sos.parentElement.appendChild(invalidContact);
  contact_sos.classList.add("is-invalid");
  contact_sos.focus();
}

// main check function
function checkForm() {
  var socialName = document.getElementById("id_social_name").value;
  var email = document.getElementById("id_email").value;
  var phone_1 = document.getElementById("id_phone_1").value;
  var phone_2 = document.getElementById("id_phone_2").value;
  var sosContact = document.getElementById("id_sos_contact").value;
  var sosPhone = document.getElementById("id_sos_phone").value;

  // checking name input
  if (socialName.length < 2 || socialName == "" || socialName === null) {
    alertNameInput();
    return false;
  }

  // checking e-mail input
  if (
    email.indexOf("@") == -1 ||
    email.indexOf(".") == -1 ||
    email == "" ||
    email == null
  ) {
    alertEmailInput();
    return false;
  }

  if (phone_1.length < 10 || phone_1 == "" || phone_1 === null) {
    alertPhoneInput("id_phone_1");
    return false;
  }

  if (phone_2.length > 0 && phone_2.length < 10) {
    alertPhoneInput("id_phone_2");
    return false;
  }

  if (sosContact) {
    if (sosPhone.length >= 0 && sosPhone.length < 10) {
      alertPhoneInput("id_sos_phone");
      return false;
    }
  }

  if (sosPhone) {
    if (sosContact == "" || sosContact == null) {
      alertSOSContactInput();
      return false;
    }
  }

  // submit after checked form
  document.getElementById("form").submit();
}

//Address filled by ZIP Code
// aplicating function in tag
let inputCep = document.querySelector("input[id=id_zip_code]");
inputCep.addEventListener("change", buscaCep);

// handlers functions
function preencheCampos(json) {
  document.querySelector("input[id=id_address]").value = json.logradouro;
  document.querySelector("input[id=id_district]").value = json.bairro;
  document.querySelector("input[id=id_complement]").value = json.complemento;
  document.querySelector("input[id=id_city]").value = json.localidade;
  document.querySelector("input[id=id_state]").value = json.uf;
}

// main function
function buscaCep() {
  let inputCep = document.querySelector("input[id=id_zip_code]");
  let cep = inputCep.value.replace("-", "");

  let url = "http://viacep.com.br/ws/" + cep + "/json";

  let xhr = new XMLHttpRequest();
  xhr.open("GET", url, true);
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4) {
      if (xhr.status == 200) preencheCampos(JSON.parse(xhr.responseText));
    }
  };
  xhr.send();
}
