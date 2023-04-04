const selectSchool = document.querySelector('#select-school ')
const classSelect = document.querySelector('#class ')
const sectionSelect = document.querySelector('#Section')
const studentName = document.querySelector('#student-names')
const studentId = document.querySelector('#student-id ')
const Table = document.querySelector('.Table')


async function captureData() {
    const url = 'http://127.0.0.1:5000/lapis/student-data/json'
    const response = await fetch(url)
    const data = await response.json()
    console.log(data);
    return JSON.parse(data);
}

async function loadData() {
    const data = await captureData()
    const schoolNames = new Set()
    const commonAppend = document.createElement("option")
    commonAppend.textContent = "Select School Name"
    commonAppend.value = "None"
    // console.log(commonAppend);
    selectSchool.append(commonAppend)
    for (let i = 0; i < data.length; i++) {
        schoolNames.add(data[i].School_name);
    }
    let schools = Array.from(schoolNames)
    for (let i = 0; i < schools.length; i++) {
        const optionTag = document.createElement('option')
        optionTag.textContent = schools[i]
        selectSchool.append(optionTag)
    }
}

loadData()

async function selectClass() {
    classSelect.innerHTML = ''
    const commonAppend = document.createElement("option")
    commonAppend.textContent = "Select Class"
    commonAppend.value = "None"
    // console.log(commonAppend);
    classSelect.append(commonAppend)

    const selectedSchool = selectSchool.value
    const data = await captureData()
    const classSet = new Set()
    for (let i = 0; i < data.length; i++) {
        if (data[i].School_name === selectedSchool) {
            classSet.add(data[i].Class)
        }
    }
    let newClassSet = Array.from(classSet)
    newClassSet = newClassSet.sort()
    for (let i = 0; i < newClassSet.length; i++) {
        const optionTag = document.createElement('option')
        optionTag.textContent = newClassSet[i]
        classSelect.append(optionTag)
    }
}

async function selectSection() {
    sectionSelect.textContent = ''
    const commonAppend = document.createElement("option")
    commonAppend.textContent = "Select Section"
    commonAppend.value = "None"
    // console.log(commonAppend);
    sectionSelect.append(commonAppend)

    const selectedClass = classSelect.value
    const data = await captureData()
    const x = new Set()

    for (let i = 0; i < data.length; i++) {
        if (data[i].Class == selectedClass && data[i].School_name == selectSchool.value) {
            x.add(data[i].Section)
        }
    }
    let mySections = Array.from(x)
    mySections = mySections.sort()
    for (let i = 0; i < mySections.length; i++) {
        const optionTag = document.createElement('option')
        optionTag.textContent = mySections[i]
        sectionSelect.append(optionTag)
    }

}

async function NameStudent() {
    studentName.innerHTML = ''
    const commonAppend = document.createElement("option")
    commonAppend.textContent = "Select Name"
    commonAppend.value = "None"
    studentName.append(commonAppend)

    const commonAppend1 = document.createElement("option")
    commonAppend1.textContent = "ALL"
    commonAppend1.value = "All"
    studentName.append(commonAppend1)

    const selectedSection = sectionSelect.value
    // console.log(selectedSection);
    const data = await captureData()
    const x = new Set()

    for (let i = 0; i < data.length; i++) {
        if (data[i].Section == selectedSection && data[i].School_name == selectSchool.value && data[i].Class == classSelect.value) {
            x.add(data[i].Name)
        }
    }

    let myNames = Array.from(x)
    myNames = myNames.sort()
    // console.log(myNames);
    for (let i = 0; i < myNames.length; i++) {
        const optionTag = document.createElement('option')
        // optionTag.value = myNames[i]
        optionTag.textContent = myNames[i]
        // console.log(optionTag);
        studentName.append(optionTag)
    }
    return myNames
}


async function createTable(){
    // studentName.innerHTML = ''
    const selectedSection = sectionSelect.value
    const data = await captureData()
    const x = new Set()

    for (let i = 0; i < data.length; i++) {
        if (data[i].Section == selectedSection && data[i].School_name == selectSchool.value && data[i].Class == classSelect.value) {
            x.add(data[i].Name)
        }
    }

    let myNames = Array.from(x)
    myNames = myNames.sort()
    for (let i = 0; i < myNames.length; i++) {
        const optionTag = document.createElement('option')
        optionTag.textContent = myNames[i]
        studentName.append(optionTag)
    }
    console.dir(studentName.value);
    Table.innerHTML = ''
    const columns = document.createElement('tr')
    const column1Name = document.createElement('th')
    const column2Name = document.createElement('th')
    const column3Name = document.createElement('th')
    const column4Name = document.createElement('th')

    column1Name.textContent = 'School Name'
    column2Name.textContent = 'Class'
    column3Name.textContent = 'Section'
    column4Name.textContent = 'Student Name'

    columns.append(column1Name)
    columns.append(column2Name)
    columns.append(column3Name)
    columns.append(column4Name)

    Table.append(columns)

    if(studentName.value == "All"){
        for(let i = 0; i < myNames.length; i++){
            const columns = document.createElement('tr')
            const column1Value = document.createElement('td')
            const column2Value = document.createElement('td')
            const column3Value = document.createElement('td')
            const column4Value = document.createElement('td')
    
            column1Value.textContent = selectSchool.value
            column2Value.textContent = classSelect.value
            column3Value.textContent = sectionSelect.value
            column4Value.textContent = myNames[i]

            columns.append(column1Value)
            columns.append(column2Value)
            columns.append(column3Value)
            columns.append(column4Value)

            Table.append(columns)
        }
    }

    else{
        const columns = document.createElement('tr')
        const column1Value = document.createElement('td')
        const column2Value = document.createElement('td')
        const column3Value = document.createElement('td')
        const column4Value = document.createElement('td')

        column1Value.textContent = selectSchool.value
        column2Value.textContent = classSelect.value
        column3Value.textContent = sectionSelect.value
        column4Value.textContent = studentName.value

        columns.append(column1Value)
        columns.append(column2Value)
        columns.append(column3Value)
        columns.append(column4Value)

        Table.append(columns)
    }

}


///////////  dropdown data for student Id  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// async function studentid(){
//     studentId.textContent = ''
//     const commonAppend = document.createElement("option")
//     commonAppend.textContent = "Select Id"
//     commonAppend.value = "None"
//     studentId.append(commonAppend)

//     const selectedId = studentId.value
//     console.log(selectedId);
//     const data = await captureData()
//     const x = new Set()

//     for(let i = 0; i < data.length; i++){
//         if(data[i].Section == sectionSelect.value &&  data[i].School_name == selectSchool.value && data[i].Class == classSelect.value && selectedName == data[i]){
//             x.add(data[i].Id)
//         }
//     }

//     let myIds = Array.from(x)
//     myIds = myIds.sort()
//     console.log(myIds);
//     for(let i = 0; i < myIds.length; i++){
//         const optionTag = document.createElement('option')
//         optionTag.textContent = myIds[i]
//         studentId.append(optionTag)
//     }
// }
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// function getName(){
//     const name = studentName.value
//     console.log(name);
//     return name
// }

// document.querySelector('.myForm').addEventListener('submit', async function(event){
//     event.preventDefault()
//     let names = await NameStudent()
//     console.dir(event.target);
//     Table.innerHTML = ''
//     const columns = document.createElement('tr')
//     const column1Name = document.createElement('th')
//     const column2Name = document.createElement('th')
//     const column3Name = document.createElement('th')
//     const column4Name = document.createElement('th')

//     column1Name.textContent = 'School Name'
//     column2Name.textContent = 'Class'
//     column3Name.textContent = 'Section'
//     column4Name.textContent = 'Student Name'

//     columns.append(column1Name)
//     columns.append(column2Name)
//     columns.append(column3Name)
//     columns.append(column4Name)

//     // console.log(selected);
//     Table.append(columns)

//     // if(getName() == "All"){
//     //     for(let i = 0; i < names.length; i++){
//     //         const columns = document.createElement('tr')
//     //         const column1Value = document.createElement('td')
//     //         const column2Value = document.createElement('td')
//     //         const column3Value = document.createElement('td')
//     //         const column4Value = document.createElement('td')
    
//     //         column1Value.textContent = selectSchool.value
//     //         column2Value.textContent = classSelect.value
//     //         column3Value.textContent = sectionSelect.value
//     //         column4Value.textContent = names[i]

//     //         columns.append(column1Value)
//     //         columns.append(column2Value)
//     //         columns.append(column3Value)
//     //         columns.append(column4Value)

//     //         Table.append(columns)
//     //     }
//     // }

//     // else{
//     //     const columns = document.createElement('tr')
//     //     const column1Value = document.createElement('td')
//     //     const column2Value = document.createElement('td')
//     //     const column3Value = document.createElement('td')
//     //     const column4Value = document.createElement('td')

//     //     column1Value.textContent = selectSchool.value
//     //     column2Value.textContent = classSelect.value
//     //     column3Value.textContent = sectionSelect.value
//     //     column4Value.textContent = studentName.value

//     //     columns.append(column1Value)
//     //     columns.append(column2Value)
//     //     columns.append(column3Value)
//     //     columns.append(column4Value)

//     //     Table.append(columns)
//     // }
// });


