document.addEventListener("DOMContentLoaded", function() {
  const popup = document.getElementById("investment-popup");
  const names = [
    "Martin Orneil","Sophia James","David Okoro","Emma Brown","Liam Chen","Olivia Rossi",
    "Carlos Mendes","Aisha Khan","John Peterson","Fatima Ali","Hiro Tanaka","Maria Lopez",
    "Kwame Boateng","Elena Petrova","Ahmed Hassan","Grace Williams","Diego Silva","Chen Wei",
    "Nora Schmidt","Samuel Johnson","Isabella Garcia","Mohammed Ibrahim","Anna Kowalski",
    "George Mensah","Laura Müller","Pedro Santos","Yuki Nakamura","Chloe Dubois","Raj Patel",
    "Sara Andersson","Ali Reza","Marta Fernandez","William Smith","Jessica Taylor","Victor Hugo",
    "Hassan Omar","Linda Chen","Stefan Novak","Patricia Brown","Daniel Kim","Angela Rossi",
    "Omar Farouk","Julia Becker","Henry Wilson","Camila Torres","Igor Ivanov","Mei Lin",
    "Kwesi Owusu","Fatou Diop","Thomas Johnson","Sofia Costa","Ahmed El-Sayed","Emily Clark"
  ];
  const countries = [
    "Scotland","Nigeria","Canada","Germany","Brazil","India","USA","South Africa","Japan","Mexico",
    "Ghana","Russia","Egypt","Italy","France","Spain","China","Kenya","Australia","Turkey",
    "Argentina","Sweden","Norway","Denmark","Finland","Poland","Ukraine","Netherlands","Belgium",
    "Portugal","Switzerland","Austria","Ireland","Morocco","Algeria","Tunisia","Saudi Arabia",
    "UAE","Qatar","Kuwait","Pakistan","Bangladesh","Sri Lanka","Nepal","Thailand","Vietnam",
    "Philippines","Indonesia","Malaysia","Singapore","Chile","Peru","Colombia","Venezuela","Ethiopia","Tanzania"
  ];

  const amounts = [100,200,300,400,500,600,750,1000,1200,1500,2000,2500,3000];
  const actions = ["made a deposit of","withdrew","registered an account with"];
  let events = [];

  function buildEvents() {
    events = [];
    for (let i = 0; i < names.length; i++) {
      const name = names[i];
      const country = countries[Math.floor(Math.random() * countries.length)];
      const amount = amounts[Math.floor(Math.random() * amounts.length)];
      const action = actions[Math.floor(Math.random() * actions.length)];

      if (action === "registered an account with") {
        events.push(`${name} from ${country} ${action} Finbit`);
      } else {
        events.push(`${name} from ${country} ${action} $${amount}`);
      }
    }
    for (let i = events.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [events[i], events[j]] = [events[j], events[i]];
    }
  }

  let index = 0;

  function showNextInvestment() {
    if (index >= events.length) {
      buildEvents(); 
      index = 0;
    }
    popup.textContent = events[index];
    popup.style.display = "block";

    setTimeout(() => {
      popup.style.display = "none";
    }, 9000); 

    index++;
  }
  buildEvents();
  setTimeout(() => {
    showNextInvestment();
    setInterval(showNextInvestment, 10000);
  }, 10000);
});
