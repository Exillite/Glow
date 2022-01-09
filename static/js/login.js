var x = document.getElementById("login");
var y = document.getElementById("register");
var z = document.getElementById("btn");
var fbox = document.getElementById("formbox");


var rbtn = document.getElementById('rbtn');


function register(){
	x.style.left = '-400px';
	y.style.left = '50px';
	z.style.left = '110px';
	fbox.style.height = '580px';
} 

function login(){
	x.style.left = '50px';
	y.style.left = '450px';
	z.style.left = '0px';
	fbox.style.height = '480px';
}

function vE(email) {
  if (email === null) {
    return false;
  }
  var re = /\S+@\S+\.\S+/;
  return re.test(email);
}


function sendReg () {

  let name = document.querySelector('#rname');
  let surname = document.querySelector('#rsurname');
  let email = document.querySelector('#remail');
  let password = document.querySelector('#rpassword');
  let passwordt = document.querySelector('#rpasswordtoo');
  var checkbox = document.getElementById('rcheckbox');  


  if (password.value.length >= 8 && password.value == passwordt.value && checkbox.checked && name.value.length >= 2 && surname.value.length >= 3 && vE(email.value)){
    // а вот сюда мы поместим ответ от сервера
    let result = document.querySelector('.result');
    // создаём новый экземпляр запроса XHR
    let xhr = new XMLHttpRequest();
    // адрес, куда мы отправим нашу JSON-строку
    let url = myip + "/api";
    // открываем соединение
    xhr.open("POST", url, true);
    // устанавливаем заголовок — выбираем тип контента, который отправится на сервер, в нашем случае мы явно пишем, что это JSON
    xhr.setRequestHeader("Content-Type", "application/json");
    // когда придёт ответ на наше обращение к серверу, мы его обработаем здесь
    xhr.onreadystatechange = function () {
      // если запрос принят и сервер ответил, что всё в порядке
      if (xhr.readyState === 4 && xhr.status === 200) {
        // выводим то, что ответил нам сервер — так мы убедимся, что данные он получил правильно
        getReg(this.responseText);
      }
    };
    // преобразуем наши данные JSON в строку
    var data = JSON.stringify({ "method": "reg", "name": name.value, "surname": surname.value, "email": email.value, "password": password.value });
    // когда всё готово, отправляем JSON на сервер
    xhr.send(data);
  } else {
    if (password.value.length <= 8) {
      notify("error","Ошибка! \nДлина пороля должна быть не менее 8 символов.");
    }
    if (password.value != passwordt.value) {
      notify("error","Ошибка! \nПароли не совпадают!");
    }
    if (checkbox.checked == false) {
      notify("error","Ошибка! \nДля регистрации необходмо дать пользовательское соглашение.");
    }
    if (name.value.length <= 2) {
      notify("error","Ошибка! \nВведите коректное имя.");
    }
    if (surname.value.length <= 3) {
      notify("error","Ошибка! \nВведите коректную фамилию.");
    }
    if (vE(email.value) == false) {
      notify("error","Ошибка! \nВведите коректный e-mail.");
    }
  }
}



function sendLogin () {
  let email = document.querySelector('#lemail');
  let password = document.querySelector('#lpassword');
  var checkbox = document.getElementById('lcheckbox');  


  if (vE(email.value) && password.value.length >= 8){
    // а вот сюда мы поместим ответ от сервера
    let result = document.querySelector('.result');
    // создаём новый экземпляр запроса XHR
    let xhr = new XMLHttpRequest();
    // адрес, куда мы отправим нашу JSON-строку
    let url = myip + "/api";
    // открываем соединение
    xhr.open("POST", url, true);
    // устанавливаем заголовок — выбираем тип контента, который отправится на сервер, в нашем случае мы явно пишем, что это JSON
    xhr.setRequestHeader("Content-Type", "application/json");
    // когда придёт ответ на наше обращение к серверу, мы его обработаем здесь
    xhr.onreadystatechange = function () {
      // если запрос принят и сервер ответил, что всё в порядке
      if (xhr.readyState === 4 && xhr.status === 200) {
        // выводим то, что ответил нам сервер — так мы убедимся, что данные он получил правильно
        getLogin(this.responseText);
      }
    };
    // преобразуем наши данные JSON в строку
    var data = JSON.stringify({ "method": "login", "email": email.value, "password": password.value, "stay": checkbox.checked});
    // когда всё готово, отправляем JSON на сервер
    xhr.send(data);
  } else {
    if (vE(email.value) == false) {
      notify("error","Ошибка! \nВведите коректный e-mail.");
    }
    if (password.value.length <= 8) {
      notify("error","Ошибка! \nВведите коректный пароль.");
    }
  }
}

function getReg (ret) {
  switch (ret) {
    case "ANCE":
      notify("error","Ошибка! \nВведите коректный e-mail.");
      break;
    case "ANCP":
      notify("error","Ошибка! \nВведите коректный пароль.");
      break;
    case "ALR":
      notify("info","Внимание! \nВы уже зарегистрированы!");
      break;
    case "ERORR":
      notify("error","Ошибка!");
      break;
    case "OK":
      window.location.href = myip + '/alreg';
      break;
    default:
      console.log('server return after reg:' + ret);
      break;
  }
}

function getLogin (ret) {
  switch (ret.split("=")[0]) {
    case "NO":
      notify("info","Вы ещё не зарегистрированы.");
      break;
    case "PAS":
      notify("error","Ошибка! \nНеверный пароль!");
      break;
    case "ALR":
      notify("info","Внимание! \nВы уже зарегистрированы!");
      break;
    case "ERORR":
      notify("error","Ошибка!");
      break;
    case "id":
      window.location.href = myip + '/';
      break;
    default: 
      console.log('server return after login:' + ret);
      break;
  }
}

