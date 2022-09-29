/* - - - INCLUDES & NAMESPACES - - - */
#include <iostream>
#include <fstream>
#include <vector>
#include <bits/stdc++.h>
#include <string>
#include <tuple>
#include <thread>
#include <future>
#include <chrono> 

//system
#include <cstdlib>

using namespace std;
using namespace std::chrono;
/*************************************/

/* - - - DEFINICIÓN DE CONSTANTES - - - */
#define LOG_FILE true    // loggear información en un archivo
#define LOG_CONSOLE false   // loggear data en la consola

#define POPULATION_SIZE 30
#define MAX_ITERATIONS 50

#define MAX_ID_LENGTH 5

#define MUTATION_TYPE 1
// mutation type:
//  - 1: Constante
//  - 2: Lineal
#define MUTATION_START_PROBABILITY 10
#define MUTATION_END_PROBABILITY 60

#define FIRST_LAYER_ALPHA   0.2
#define SECOND_LAYER_ALPHA  0.2
#define THIRD_LAYER_ALPHA   0.2
#define HAT_ALPHA           0.2
#define PANTS_ALPHA         0.2
#define SHOES_ALPHA         0.2

#define DIVERSITY_TYPE 2
// 1: by cloth_id ; 2: by hamming distance 

#define ALPHA 0.9 // ponderación: \alpha * P(c) + (1-\alpha) * nota


/****************************************/

/* - - - UTILS - - - */

// da formato al id dado el largo del mayor id (5 dígitos)
string formatId(int id) {
    string id_string = to_string(id);
    while (id_string.length() < MAX_ID_LENGTH) {
        id_string = "0" + id_string;
    }
    return id_string;
}

/*
 * randomNumber: Función que genera números aleatorios en un rango dado
 *  + parámetros:
 *      (int) start: punto de inicio para el rango de números deseados
 *      (int)   end: punto de término para el rango de números deseados
 *  + retorno:
 *      (int) un número aleatorio en el rango [a, b]
 */
int randomNumber(int start, int end) {
    int range = (end - start)+1;
    int random_int = start + ( rand() % range );
    return random_int;
}

// retorna un booleano aleatorio
bool getRandomBool() {
    return randomNumber(0, 1) == 0;
}

// retorna un elemento aleatorio de la lista list.
// Si la flag es false, entonces podría retornar un elemento vacío "000..." (no forma parte de la lista).
// Si la flag es false, entonces retorna siempre un elemento de la lista list
int getRandomElem(vector<int> const &prendas_disponibles, bool flag = false) {
    int id_elemento = 0;
    // si es que la flag es false:
    //  solo puede tener el elemento si es que el randombool es true
    // si es que la flag es true:
    //  siempre tendrá un elemento
    if (flag || getRandomBool()) { // aleatoriamente decidir si tendrá o no el elemento
        int random_index = rand() % prendas_disponibles.size();
        id_elemento = prendas_disponibles[random_index];
    }

    return id_elemento;
}

int linealProbability(int t) {
    // ecuación de la recta
    int iteration_probability = ( (MUTATION_END_PROBABILITY - MUTATION_START_PROBABILITY) / (MAX_ITERATIONS - 0) ) * ( t - 0 ) + MUTATION_START_PROBABILITY;
    return iteration_probability;
}

// Obtener un sombrero aleatorio (podría retornar una secuencia vacía "000...")
int getHat(vector<int> const &gorros_disponibles) {
    return getRandomElem(gorros_disponibles);
}

// Obtener un par de zapatos aleatorios (siempre retorna una prenda válida)
int getShoes(vector<int> const &zapatos_disponibles) {
    return getRandomElem(zapatos_disponibles, true);
}

// Obtener un par de pantalones aleatorio (siempre retorna una prenda válida)
int getPants(vector<int> const &pantalones_disponibles) {
    return getRandomElem(pantalones_disponibles, true);
}

// Obtener una prenda de primera capa aleatoria (siempre retorna una prenda válida)
int getFirstLayer(vector<int> const &primeraCapa_disponibles) {
    return getRandomElem(primeraCapa_disponibles, true);
}

// Obtener una prenda de segunda capa aleatoria (podría retornar una secuencia vacía "000...")
int getSecondLayer(vector<int> const &segundaCapa_disponibles) {
    return getRandomElem(segundaCapa_disponibles);
}

// Obtener una prenda de segunda capa aleatoria (podría retornar una secuencia vacía "000...")
int getThirdLayer(vector<int> const &terceraCapa_disponibles) {
    return getRandomElem(terceraCapa_disponibles);
}

// Lee el archivo con los atributos de cada prenda y retorna un mapeo, donde la llave corresponde al id de la
// prenda y el valor asociado corresponde a su vector de características
map<int, vector<int>> read_record(string filename) {
	fstream fin;
	fin.open(filename, ios::in);
	vector<int> row;
	string line, word;
    bool isFirstLine = true; 
    vector<vector<int>> listado;
    map<int, vector<int>> armario;
    armario[0] = vector<int>({0,0,0,0,0,0,0,0,0,0,0,0,0,0});

	while (fin >> line) {
        if (isFirstLine) isFirstLine = false;
        else {
	        row.clear();
		    stringstream s(line);
            bool isId = true; 
            int id_cloth;
		    while (getline(s, word, ',')) {
                if (isId) { 
                    id_cloth = stoi(word);
                    isId = false;
                }
                else
                    row.push_back(stoi(word));
            }
            armario.insert( {id_cloth, row} );
		}
    }
    return armario;
}

// Lee el archivo con la clasificación predecida para el outfit con id `id`.
vector<double> read_output_file(int id) {
    vector<double> output;
    fstream file;
    string nomarch = "./Output_Files/output_file_" + to_string(id) + ".txt";
    auto filename = nomarch.c_str();


    file.open(filename,ios::in); //open a file to perform read operation using file object
    if (file.is_open()){ //checking whether the file is open
        string tp;
        while(getline(file, tp)){ //read data from file object and put it into string.
           output.push_back( stof( tp ) ); //print the data of the string
        }
        file.close(); //close the file object.
    }
    return output;
}

// convierte un vector de enteros en un string que codifica la misma información
string vectorToString(vector<int> vector) {
    stringstream ss;
    copy( vector.begin(), vector.end(), ostream_iterator<int>(ss, ","));
    string s = ss.str();
    return s.substr(0, s.length() - 1);
}

/***********************************/

/* - - - DEFINICIÓN DE CLASE - - - */
/*
 * CLASE Outfit: Corresponde a los individuos de la población para el algoritmo
 * genético. 
 */
class Outfit {
    public:
        int id;
        int nota;
        float probabilidad;

        float fitness;
        float diversidad;

        int id_firstLayer;
        int id_secondLayer;
        int id_thirdLayer;
        int id_hat;
        int id_shoes;
        int id_pants;

        vector<int> features_firstLayer;
        vector<int> features_secondLayer;
        vector<int> features_thirdLayer;
        vector<int> features_hat;
        vector<int> features_shoes;
        vector<int> features_pants;

        Outfit(int id_outfit, map<int, vector<int>> const &cateogrias, map<int, vector<int>> const &prendas);
        Outfit(int id_outfit, int id_firstLayer, int id_secondLayer, int id_thirdLayer, int id_hat, int id_shoes, int id_pants, map<int, vector<int>> const &prendas);
        
        void set_id_for_category(int id, int category, map<int, vector<int>> const &prendas_disponibles);
        
        tuple<Outfit, Outfit> mate(Outfit outfit2, map<int, vector<int>> const &prendas);
        Outfit mutate(int t, map<int, vector<int>> const &armario, map<int, vector<int>> const &prendas);

        void leer_resultados(int weather_category);
        double calcFitness(bool diversity_control);
        double calcularDiversidad(vector<Outfit> const &population);
};

// Setea la propiedad adecuada de la clase en dependencia de la categría ingresada como parámetro.
// adicionalmente setea el vector de características asociado a ese id
void Outfit::set_id_for_category(int const id, int const category, map<int, vector<int>> const &prendas_disponibles) {
            vector<int> const cloth_features = prendas_disponibles.at(id);

            switch (category) {
                case 1: 
                    this->id_firstLayer = id;
                    this->features_firstLayer = cloth_features;
                    break;
                case 2: 
                    this->id_secondLayer = id;
                    this->features_secondLayer = cloth_features;
                    break;
                case 3: 
                    this->id_thirdLayer = id;
                    this->features_thirdLayer = cloth_features;
                    break;
                case 4: 
                    this->id_hat = id;
                    this->features_hat = cloth_features;
                    break;
                case 5: 
                    this->id_shoes = id;
                    this->features_shoes = cloth_features;
                    break;
                case 6: 
                    this->id_pants = id;
                    this->features_pants = cloth_features;
                    break;
            }
        }

string showVector(vector<int> const &v) {
    string s = "";
    for (int e: v) {
        s += to_string(e) + " ";
    }
    return s;
}

// Overloading del operador "<" 
bool operator<(const Outfit &o1, const Outfit &o2) {
    return o1.fitness < o2.fitness;
}

// Overloading del operador ">"
bool operator>(const Outfit &o1, const Outfit &o2) {
    return o1.fitness > o2.fitness;
}

// Overloading del operador "<<"
ostream& operator<<(ostream& os, Outfit &o) {
    os << "Outfit id: " << o.id << " | f: " << o.fitness << " | d: " << o.diversidad << " | p: " << o.probabilidad << " | n: " << o.nota <<  endl;
    os << "\t1: " << formatId(o.id_firstLayer) << " | " << showVector(o.features_firstLayer) << endl;
    os << "\t2: " << formatId(o.id_secondLayer) << " | " << showVector(o.features_secondLayer) << endl;
    os << "\t3: " << formatId(o.id_thirdLayer) << " | " << showVector(o.features_thirdLayer) << endl;
    os << "\t4: " << formatId(o.id_hat) << " | " << showVector(o.features_hat) << endl;
    os << "\t5: " << formatId(o.id_shoes) << " | " << showVector(o.features_shoes) << endl;
    os << "\t6: " << formatId(o.id_pants) << " | " << showVector(o.features_pants) << endl;
    return os;
}

/* - - - - - - LOGGERS - - - - - -*/
/*
 * LogMutation: Función que escribe en un pipeline de salida la data referente a una mutación por
 * un individuo. Si la constante LOG_FILE es true, escribe la data en un archivo "logs.txt". Si la
 * constante LOG_CONSOLE es true, escribe la data en la consola. Las constantes no son excluyentes, por
 * lo que se podría escribir la data en ambos pipelines.
 *  + parámetros:
 *      (int)                id: identificador único del individuo en la generación
 *      (string) old_chromosome: chromosoma original del individuo
 *      (string)     chromosome: chromosoma después de la mutación
 *      (int)       old_fitness: fitness original del individuo
 *      (int)           fitness: fitness después de la mutación
 *  + retorno: -
 */
void LogMutation(Outfit const &o, int const id_old_cloth, int const id_mutated_cloth, int const category_mutated) {
    // cout << "logging out the info" << endl;
    if (LOG_FILE) {
        ofstream file;
        // modo "a"
        file.open ("logs.txt", std::ios_base::app | std::ios_base::in);
        file << "- Mutación -" << endl;
        file << "Se mutó el individuo " << o.id << endl;
        file << "Categoría: " << category_mutated << endl;
        file << id_old_cloth << " -> " << id_mutated_cloth << endl << endl;
        file.close();
    }

    if (LOG_CONSOLE) {    
        cout << "- Mutación -" << endl;
        cout << "Se mutó el individuo " << o.id << endl;
        cout << "Categoría: " << category_mutated << endl;
        cout << id_old_cloth << " -> " << id_mutated_cloth << endl << endl;
    }
}

/*
 * LogCrossOver: Función que escribe en un pipeline de salida la data referente a un cruzamiento entre
 * dos individuos. Si la constante LOG_FILE es true, escribe la data en un archivo "logs.txt". Si la 
 * constante LOG_CONSOLE es true, escribe la data en la consola. Las constantes no son excluyentes, por
 * lo que se podría escribir la data en ambos pipelines.
 * + parámetros:
 *      (Outfit) parent1: primer padre participante en el cruzamiento
 *      (Outfit) parent2: segundo padre participante en el cruzamiento
 *      (Outfit)  child1: primer hijo resultante del cruzamiento
 *      (Outfit)  child2: segundo hijo resultante del cruzamiento
 *      (int)      index: posición en la que se realizó el cruzamiento
 * + retorno: -
 */
void LogCrossOver(Outfit &parent1, Outfit &parent2, Outfit const &child1, Outfit const &child2) {
    if (LOG_FILE) {
        ofstream file;
        file.open("logs.txt", std::ios_base::app | std::ios_base::in);
        file << "\t- Cruzamiento -" << endl;
        file << parent2 << endl << endl;
        file << parent1 << endl << endl;
        
        file.close();
    }
    if (LOG_CONSOLE) {
        cout << "\t- Cruzamiento -" << endl;
        cout << parent1 << endl << endl;
        cout << parent2 << endl << endl;
        // cout << "\tHijos:" << endl;
        // cout << child1 << endl << endl;
        // cout << child2 << endl << endl;
    }
}

/*
 * LogGeneration: Función que escribe en un pipeline de salida la data referente a una generación.
 * Si la constante LOG_FILE es true, escribe la data en un archivo "logs.txt". Si la constante LOG_FILE
 * LOG_CONSOLE es true, escribe la data en la consola. Las constantes no son excluyentes, por lo que se est
 * podía escribir la data en ambos pipelines.
 *  + parámetros:
 *      (vector<Outfit>) P: conjunto de individuos (población)
 *      (int)            g: número de generación
 *  + retorno: -
 */
void LogGeneration(vector<Outfit> &P, int g, float diversidad) {
    ofstream f1;
    f1.open("diversity_vs_generation.txt", std::ios_base::app | std::ios_base::in);
    f1 << g << "," << diversidad << endl;
    f1.close();
    if (LOG_FILE) {
        ofstream file;
        file.open ("logs.txt", std::ios_base::app | std::ios_base::in);
        file << "---------- GENERACIÓN " << g << " | Diversidad: " << diversidad << " ----------" << endl;
        for (int i = 0; i < POPULATION_SIZE; i++) {
            file << P.at(i) << endl;
        }
        file << "-----------------------------------------------------------------" << endl << endl;
        file.close();
    }
    if (LOG_CONSOLE) {
        cout << "---------- GENERACIÓN " << g << " | Diversidad: " << diversidad << " ----------" << endl;
        for (int i = 0; i < POPULATION_SIZE; i++) {
            cout << P[i] << endl;
        }
        cout << "-----------------------------------------------------------------" << endl << endl;
    }
}
/**********************************/

// Constructores
Outfit::Outfit(
    int id_outfit,
    int id_firstLayer,
    int id_secondLayer,
    int id_thirdLayer,
    int id_hat,
    int id_shoes,
    int id_pants,
    map<int, vector<int>> const &prendas)  
{   
    set_id_for_category(id_firstLayer, 1, prendas);
    set_id_for_category(id_secondLayer, 2, prendas);
    set_id_for_category(id_thirdLayer, 3, prendas);
    set_id_for_category(id_hat, 4, prendas);
    set_id_for_category(id_shoes, 5, prendas);
    set_id_for_category(id_pants, 6, prendas);

    this->id = id_outfit;    
}

Outfit::Outfit(int id_outfit, map<int, vector<int>> const &categorias, map<int, vector<int>> const &prendas) {  
    this->id_firstLayer = getFirstLayer(categorias.at(1));
    this->id_secondLayer = getSecondLayer(categorias.at(2));
    this->id_thirdLayer = getThirdLayer(categorias.at(3));
    this->id_hat = getHat(categorias.at(4));
    this->id_shoes = getShoes(categorias.at(5));
    this->id_pants = getPants(categorias.at(6));

    set_id_for_category(id_firstLayer, 1, prendas);
    set_id_for_category(id_secondLayer, 2, prendas);
    set_id_for_category(id_thirdLayer, 3, prendas);
    set_id_for_category(id_hat, 4, prendas);
    set_id_for_category(id_shoes, 5, prendas);
    set_id_for_category(id_pants, 6, prendas);

    this->id = id_outfit;  
}
// ----

// invoca el proceso del clasificador `classify.py` con el genoma del vestuario `o`
void NNclassify(Outfit const &o, string modelo) {
    char command[1024];
    strcpy(command, "python3.7 classify.py ");

    string id = to_string(o.id);

    strcat(command, id.c_str());
    strcat(command, " ");

    // char features_string[o.features_firstLayer.size()];

    string r = vectorToString(o.features_firstLayer);
    strcat(command, r.c_str());
    strcat(command, " ");

    r = vectorToString(o.features_secondLayer);
    strcat(command, r.c_str());
    strcat(command, " ");

    r = vectorToString(o.features_thirdLayer);
    strcat(command, r.c_str());
    strcat(command, " ");

    r = vectorToString(o.features_hat);
    strcat(command, r.c_str());
    strcat(command, " ");

    r = vectorToString(o.features_shoes);
    strcat(command, r.c_str());
    strcat(command, " ");

    r = vectorToString(o.features_pants);
    strcat(command, r.c_str());
    strcat(command, " ");

    strcat(command, modelo.c_str());
    // strcat(command, " ");

    // printf("command: %s\n", command);

    system(command);
    // cout << "fitness for outfit " << id << " calculated" << endl;
}

// Calcular Fitness / Función de Evaluación
double Outfit::calcFitness(bool diversity_control) {
    double f = (this->probabilidad * ALPHA) + ( (this-> nota / 5.0) * (1 - ALPHA) );
    if (diversity_control) f += diversidad;
    this->fitness = f;

    return fitness;
}

/*
 * Outfit::leer_resultados: Obtiene las probabilidades de que el vestuario pertenezca a cada una de las categorías de clima.
 * Le resta la probabilidad de las categorías exclusivas asociadas a la categoría de clima actual.
 * El vector de categorías es el siguiente:
 *      0: nota       
 *      1: isCold 
 *      2: isRainy
 *      3: isWet
 *      4: isTempered
 *      5: isHot
 *  + parámetros: -
 *  + retorno: 
 */
void Outfit::leer_resultados(int weather_category) {
    vector<double> c_vector = read_output_file(id);
    double probabilidad = c_vector[ weather_category ];

    if (weather_category == 1) {
        probabilidad -= (c_vector[5] + c_vector[3])/2;
    } 
    if (weather_category == 2) {
        probabilidad -= (c_vector[4] + c_vector[5])/2;
    }
    if (weather_category == 3) {
        probabilidad -= (c_vector[4] + c_vector[1])/2;
    }
    if (weather_category == 4) {
        probabilidad -= (c_vector[3] + c_vector[2])/2;
    }
    if (weather_category == 5) {
        probabilidad -= (c_vector[1] + c_vector[2])/2;
    }
    // isRainy isCold isTempered isHot isWet
    // 2        1     4           5      3
    this->probabilidad = probabilidad;
    this->nota = c_vector[0];

    //double fitness = probabilidad * ALPHA + (nota/5) * (1 - ALPHA);

    // if (diversity_control) fitness += diversidad;

    // this->fitness = fitness;

    // return fitness;
}

// Cruzar dos individuos
/*
 * Outfit::mate: Función que cruza al individuo que invoca el método, con otro individuo. El cruzamiento implementado 
 * actualmente corresponde al cruzamiento en un punto (aleatorio).
 * + parámetros: 
 *      (Outfit) outfit2: segundo individuo involucrado en el cruzamiento
 * + retorno:
 *      (Outfit) primer hijo resultante del cruzamiento
 *      (Outfit) segundo hijo resultante del cruzamiento
 *      (int)    posición aleatoria en la que se realizó el cruzamiento
 */
tuple<Outfit, Outfit> Outfit::mate(Outfit o2, map<int, vector<int>> const &prendas) {

    Outfit child1 = Outfit(
        this->id,
        this->id_firstLayer, 
        this->id_secondLayer, 
        this->id_thirdLayer,
        o2.id_hat, 
        o2.id_shoes, 
        o2.id_pants, 
        prendas
    );

    Outfit child2 = Outfit(
        o2.id,
        o2.id_firstLayer, 
        o2.id_secondLayer, 
        o2.id_thirdLayer,
        this->id_hat, 
        this->id_shoes, 
        this->id_pants, 
        prendas
    );
    
    LogCrossOver(*this, o2, child1, child2);

    return {child1, child2};
}

// Mutar un individuo
/*
 * Outfit::mutate: Función que muta al individuo que invoca al método. La mutación corresponde al reemplazo de un 
 * secuencia de chromosoma de prenda aleatoria, por otro cromosoma de una prenda de la misma categoria. Si es que la prenda a la que se está
 * intentando mutar no existe dentro del conjutno (cadena de 0), entonces no se muta.
 * Luego calcula la nueva fitness del individuo
 *  + parámetros: -
 *  + retorno: -
 */
Outfit Outfit::mutate(int t, map<int, vector<int>> const &armario, map<int, vector<int>> const &prendas) {
    // cout << "mutando al individuo:" << this->id << endl;
    
    int p = rand() % 100;
    p = 0;

    int iteration_probability;

    if (MUTATION_TYPE == 1) {
        // probabilidad constante
        iteration_probability = MUTATION_START_PROBABILITY;
    }
    else if (MUTATION_TYPE == 2) {
        // probabilidad lineal
        iteration_probability = linealProbability(t);
    }

     Outfit mutacion = Outfit(
        this->id,
        this->id_firstLayer,
        this->id_secondLayer,
        this->id_thirdLayer,
        this->id_hat,
        this->id_shoes,
        this->id_pants,
        prendas
    );

    if (p > iteration_probability) return mutacion;

    // Mutar
    int random_category = rand() % 6 + 1;
    
    // flag que indica si es que el randomElem podría entregar "00000..."
    bool flag = true;
    int id_mutated_cloth;
    switch (random_category) {
        case 1:
            id_mutated_cloth = this->id_firstLayer;
            break;
        case 2:
            id_mutated_cloth = this->id_secondLayer;
            flag = false;
            break;
        case 3:
            id_mutated_cloth = this->id_thirdLayer;
            flag = false;
            break;
        case 4:
            id_mutated_cloth = this->id_hat;
            flag = false;
        case 5:
            id_mutated_cloth = this->id_shoes;
            break;
        case 6:
            id_mutated_cloth = this->id_pants;
            break;
    } 

    // seleccionar una prenda aleatoria de la misma categoría
    // también podría asignar eliminar dicha prenda si es que no es esencial (hat, 2layer, 3layer)
    
    int id_random_cloth = id_mutated_cloth;
    while (id_mutated_cloth == id_random_cloth) {
        id_random_cloth = getRandomElem( armario.at(random_category), flag );
    }

    mutacion.set_id_for_category(id_random_cloth, random_category, prendas);

    LogMutation(*this, id_random_cloth, id_mutated_cloth, random_category);

    return mutacion;
}
/****************************************/

/*
 * Populate: Función que genera una población aleatoria de individuos, con tamaño POPULATION_SIZE.
 *  + parámetros:
 *      (int) t: no se utiliza pero podría ser útil
 *  + retorno:
 *      (vector<Outfit>) conjunto de individuos generados
 */
vector<Outfit> Populate(int t, map<int, vector<int>> const &categorias, map<int, vector<int>> const &prendas_disponibles) {
    vector<Outfit> population;
    for (int i = 0; i < POPULATION_SIZE; i++) {
        Outfit newOutfit = Outfit(i, categorias, prendas_disponibles);
        // cout << newOutfit << endl;
        population.push_back(newOutfit);
    }

    /*
    for (int i = 0; i < population.size(); i++) {
        population[i].calculate_hamming_distance(population);
    }
    */

    return population;
}

/*
 * EndingCondition: Función que verifica la condición de término para el ciclo principal.
 * Puede ser por iteraciones máximas, por encontrar la mejor solución, por convergencia, etc.
 */
bool EndingCondition(int t, const Outfit o) {
    // if (o.fitness == 0) return true;
    return t ==  MAX_ITERATIONS;
}

// Clasifica los vestuarios de los individuos con index \in [start, ..., end]
// función invocada por las hebras
void NNmultiClassify(vector<Outfit> const &P, int start, int end, string const modelo) {

    for (int i = start; i <= end; i++) {
        NNclassify( P.at(i), modelo );
    }

}

// calcula la diversidad entre dos vestuarios `o` y `o2`
double diversity_by_id(Outfit const &o, const Outfit &o2) {
    double sum = 0.0;
    int cloth_count = 3;

    if (o.id_firstLayer != o2.id_firstLayer) sum += 1;
    if (o.id_pants != o2.id_pants) sum += 1; 
    if (o.id_shoes != o2.id_shoes) sum += 1;

    if ( !(o.id_secondLayer == 0 && o2.id_secondLayer == 0) ) {
        if (o.id_secondLayer != o2.id_secondLayer)
            sum += 1;
        cloth_count++;
    }

    if ( !(o.id_thirdLayer == 0 && o2.id_thirdLayer == 0) ) {
        if (o.id_thirdLayer != o2.id_thirdLayer)
            sum += 1;
        cloth_count++;
    }

    if ( !(o.id_hat == 0 && o2.id_hat == 0) ) {
        if (o.id_hat != o2.id_hat)
            sum += 1;
        cloth_count++;
    }
    
    return sum / cloth_count;
}

// calcula la distancia de hamming entre dos vectores de características (features) `a` y `b`
// (entre dos prendas del mismo tipo)
double hamming_distance_aux(vector<int> const &a, vector<int> const &b) {
    float sum = 0.0;
    for (unsigned int i = 1; i < a.size(); i++) {
        if (a[i] != b[i]) sum += 1;
    }
    return sum / (a.size() - 1);
}

// calcula la distancia de hamming entre dos vestuarios, para cada una de sus prendas
double hamming_distance(Outfit const &o1, Outfit const &o2) {
    double sum = 0.0;
    int cloth_count = 3;

    sum += hamming_distance_aux(o1.features_firstLayer, o2.features_firstLayer);
    sum += hamming_distance_aux(o1.features_shoes, o2.features_shoes);
    sum += hamming_distance_aux(o1.features_pants, o2.features_pants);

    if ( !(o1.id_secondLayer == 0 && o2.id_secondLayer == 0) ) {
        sum += hamming_distance_aux(o1.features_secondLayer, o2.features_secondLayer);
        cloth_count++;
    }

    if ( !(o1.id_thirdLayer == 0 && o2.id_thirdLayer == 0) ) {
        sum += hamming_distance_aux(o1.features_thirdLayer, o2.features_thirdLayer);
        cloth_count++;
    }

    if ( !(o1.id_hat == 0 && o2.id_hat == 0) ) {
        sum += hamming_distance_aux(o1.features_hat, o2.features_hat);
        cloth_count++;
    }

    return sum / cloth_count;
}

// calcula la diversidad de un vestuario para toda su generación
double Outfit::calcularDiversidad(vector<Outfit> const &V) {
    double sum_diversity = 0.0;
    for (unsigned int i = 0; i < V.size(); i++) {
        switch (DIVERSITY_TYPE) {
            case 1: // por id
                sum_diversity += diversity_by_id(*this, V[i]);
                break;
            case 2: // por distancia de hamming
                sum_diversity += hamming_distance(*this, V[i]);
                break;
        }
    }
    this->diversidad = sum_diversity / POPULATION_SIZE;
    return sum_diversity;

}

// calcula la diversidad para todos los vestuarios existentes en la población `population`
float CalcularDiversidad(vector<Outfit> &population) {
    // calcular diversidad para cada individuo respecto a su generación
    // almacenar la suma de la diversidad de cada individuo
    float diversidad_total = 0.0;
    for (int i = 0; i < POPULATION_SIZE; i++) {
        diversidad_total += population[i].calcularDiversidad(population);
    }

    diversidad_total = diversidad_total / POPULATION_SIZE;
    return diversidad_total;
}

// calcula la suma entre los fitness y la diversidad de cada individo de la población `population`
double CalcularFitness(vector<Outfit> &population, bool diversity_control) {
    double fitness_total = 0.0;
    double f;
    for (int i = 0; i < POPULATION_SIZE; i++) {
        f = population[i].calcFitness(diversity_control);
        fitness_total += f + 1;
    }
    return fitness_total;
}

// calcula la aptitud (revisa los archivos) para cada uno de los vestuarios existentes en la población `population` 
void LeerResultados(vector<Outfit> &population, int const weather_category) {
    for (int i = 0; i < POPULATION_SIZE; i++) {
        population[i].leer_resultados(weather_category);
    }
}

// Evalúa a todos los individuos de la población, calculando su fitness y su diversidad
// retorna la diversidad de la generación
float Evaluate(vector<Outfit> &population, int const weather_category, string const modelo, bool diversity_control) {
    //-std=c++11 -pthread
    thread t1(NNmultiClassify, population, 0, 4, modelo);
    thread t2(NNmultiClassify, population, 5, 9, modelo);
    thread t3(NNmultiClassify, population, 10, 14, modelo);
    thread t4(NNmultiClassify, population, 15, 19, modelo);
    thread t5(NNmultiClassify, population, 20, 24, modelo);
    thread t6(NNmultiClassify, population, 25, 29, modelo);

    t1.join();
    t2.join();
    t3.join();
    t4.join();
    t5.join();
    t6.join();

    LeerResultados(population, weather_category);

    // calcula la diversidad promedio entre los individuos de la generación
    float diversidad_generacion = CalcularDiversidad(population);
    cout <<"diversidad generacion "<<diversidad_generacion<< endl;
    
    // calcula el fitness considerando la nota y la probabilidad de un vestuario
    CalcularFitness(population, false);

    //ordenar de mayor a menor
    sort(population.begin(), population.end(), std::greater<Outfit>());
    return diversidad_generacion;    
}

// retorna la posición (index) del individuo seleccionado mediante método ruleta de la fortuna
// la cual es una selección de manera proporcional a la aptitud y diversidad de cada individuo
int roulette_wheel_selection(vector<Outfit> const &population, float totalFitness) {
    double offset = 0.0;


    double random_number = static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/totalFitness));
    for (int i = 0; i < POPULATION_SIZE; i++) {
        offset += population[i].fitness + 1;
        if (random_number < offset) {
            return i;
        }
    }
    return POPULATION_SIZE-1;
}

void diversidadRespectoVector(vector<Outfit> &P, vector<Outfit> &V) {
    for (int i = 0; i < POPULATION_SIZE; i++) {
        P[i].calcularDiversidad(V);
    }
}

/*
 * CrossOver: Función que realiza el cruzamiento entre los individuos seleccionados de la población.
 * Se realiza cruzamiento POPULATION_SIZE / 2 veces, los padres son seleccionados de manera aleatoria de entre
 * los individuos con mejor fitness dentro del rango delimitado por ELITISM_THRESHOLD
 *  + parámetros:
 *      (vector<Outfit>) parents: conjunto de individuos a cruzar
 *  + retorno: 
 *      (vector<Outfit>) conjunto de hijos producidos en el cruzamiento
 */
vector<Outfit> CrossOver(vector<Outfit> parents, map<int, vector<int>> const &prendas, bool const diversity_control) {
    vector<Outfit> offspring;
    double totalFitness;

    vector<Outfit> elegidos;

    for (int i = 0; i < POPULATION_SIZE / 2; i++) {
        diversidadRespectoVector(parents, elegidos);
        totalFitness = CalcularFitness(parents, diversity_control);
        int r1 = roulette_wheel_selection(parents, totalFitness);
        elegidos.push_back(parents[r1]);

        diversidadRespectoVector(parents, elegidos);   
        // cout << "r1="<< r1 << " es diferente a 8" << endl;

        // cout << "diversidad individuo ya escogido: " << parents[r1].diversidad << endl;
        // cout << "diversidad de otro random: " << parents[8].diversidad << endl;

        totalFitness = CalcularFitness(parents, diversity_control);
        int r2 = roulette_wheel_selection(parents, totalFitness);
        elegidos.push_back(parents[r2]);

        auto children = parents[r1].mate(parents[r2], prendas);

        LogCrossOver(parents[r1], parents[r2], get<0>(children), get<1>(children));

        offspring.push_back(get<0>(children));
        offspring.push_back(get<1>(children));
    }


    for (int i = 0; i < POPULATION_SIZE; i++) {
        offspring[i].id = i;
    }

    return offspring;
}

/*
 * Mutate: Función que intenta realizar una mutación a cada individuo de la población y luego agrega al nuevo individuo 
 * (que podría no haber sufrido ningún cambio) y lo agrega al conjunto para la nueva generación
 *  + parámetros:
 *      (vector<Outfit>)        offspring: conjunto de individuos a los que aplicar mutación
 *      (vector<Outfit> *) new_generation: posición de memoria que almacena los individuos para la siguiente generación
 *  + retorno:
 *      (vector<Outfit>) conjutno de original de individuos pero algunos con mutaciones
 */
vector<Outfit> Mutate(vector<Outfit> offspring, int t, map<int, vector<int>> const &armario, map<int, vector<int>> const &prendas) {
    vector<Outfit> newGeneration;
    for (int i = 0; i < POPULATION_SIZE; i++) {
        Outfit mutacion = offspring[i].mutate(t, armario, prendas);
        mutacion.id = i;
        newGeneration.push_back( mutacion );
    }
    return newGeneration;
}

// Imprime un armario
void printArmario(map<int, vector<int>> const &armario) {
    for (auto const pair: armario) {
        cout << "{" << pair.first << ": "; 
        for (int i: pair.second) {
            cout << i << " ";
        }
        cout << "}"<< endl;
    }
}

// Organiza el armario en prendas por categoría
map<int, vector<int>> organizarArmario(map<int, vector<int>> const &armario) {
    map<int, vector<int>> armario_organizado;

    for (auto const pair: armario) {
        int category = pair.second[0];
        // si no existe la categoría en el diccionario 
        if (armario_organizado.count(category) == 0) {
            armario_organizado.insert( {category, vector<int>() } );
        }

        // insertar id en la cateogría correspondiente
        armario_organizado.at(category).push_back(pair.first); 
    }
    return armario_organizado;
}

// verifica si dos atuendos son idénticos o no mediante la comparación de id's para cada una de las prendas que lo componen
bool isEqual(Outfit const &o1, Outfit const &o2) {
    if (o1.id_firstLayer != o2.id_firstLayer) return false;
    if (o1.id_shoes != o2.id_shoes) return false;
    if (o1.id_pants != o2.id_pants) return false;

    if (!( o1.id_secondLayer == 0 && o2.id_secondLayer == 0) ) {
        if (o1.id_secondLayer != o2.id_secondLayer) return false;
    }
    
    if (!( o1.id_thirdLayer == 0 && o2.id_thirdLayer == 0) ) {
        if (o1.id_thirdLayer != o2.id_thirdLayer) return false;
    }
    
    if (!( o1.id_hat == 0 && o2.id_hat == 0) ) {
        if (o1.id_hat != o2.id_hat) return false;
    }

    return true;
}

// verifica si un atuendo `o` existe dentro de una lista `L`
bool checkElemInList(Outfit const &o, vector<Outfit> const &List) {
    for (Outfit elem: List) {
        if (isEqual(o, elem)) return true;
    }
    return false;
}

// escribe el conjunto de soluciones no repetidas de la última generación al archivo `finalSolutions.txt`
void writeFinalSolutions(vector<Outfit> const &population, int const weather_category) {
    vector<Outfit> selectedSolutions;
    for (Outfit o: population) {
        if (!checkElemInList(o, selectedSolutions)) {
            selectedSolutions.push_back(o);
        }
    }
    ofstream file;
    // modo "a"
    file.open ("finalSolutions.txt", std::ios_base::app | std::ios_base::in);
    file << "idC1,idC2,idC3,idC4,idC5,idC6,id,F," << weather_category << endl;
    for (Outfit o: selectedSolutions) {
        file << o.id_firstLayer << " ";
        file << o.id_secondLayer << " ";
        file << o.id_thirdLayer << " ";
        file << o.id_hat << " ";
        file << o.id_shoes << " ";
        file << o.id_pants << " ";
        file << o.id << " ";
        file << o.fitness << endl;
    }
    file.close();   
}

// genera un directorio cuyo nombre sigue el formato
//      CATEGORIA_dXX-MXX-AXXXX_HXX-mXX
// que indica la categoría de climas a los cuales son solución, el día, mes y año; y hora de la solución 
void generateOutfitFolder(vector<Outfit> const &population, int weather_category, string modelo, bool diversity_control) {
    //ordenar de mayor a menor
    writeFinalSolutions(population, weather_category);

    string d_c = "DiversityControl";
    if (!diversity_control) d_c = "NotDiversityControl";

    char command[1024];
    strcpy(command, "python3.7 generate_outfits.py ");

    strcat(command, to_string(weather_category).c_str());
    strcat(command, " ");

    strcat(command, modelo.c_str());
    strcat(command, " ");

    strcat(command, d_c.c_str());

    cout << command << endl;
    system(command);
    cout << "Outfit folders created." << endl;
}

int main(int argc, char *argv[]) {

    int weather_category = atoi(argv[1]);
    string modelo = argv[2];
    int d_c = atoi(argv[3]);
    bool diversity_control = d_c == 1;

    srand(time(NULL));

    cout << "Algoritmo Genético para categoría " << weather_category << endl;
    cout << "Utilizando modelo " << modelo << endl;
    auto prendas_disponibles = read_record("clothes.csv");
    // printArmario(prendas_disponibles);
    auto armario_organizado = organizarArmario(prendas_disponibles);
    // printArmario(armario_organizado);
    int t = 0;

    vector<Outfit> population = Populate(t, armario_organizado, prendas_disponibles);

    float diversidad_generacion = Evaluate(population, weather_category, modelo, diversity_control);

    LogGeneration(population, t, diversidad_generacion);


    // auto start = chrono::high_resolution_clock::now();
    // auto stop = chrono::high_resolution_clock::now();
    // auto duration = chrono::duration_cast<seconds>(stop - start);
    // cout << duration.count() << endl;
    
    while (!EndingCondition(t, population[0])) { // Mientras no se cumpla condición de término
        cout << "Evaluando generación " << t << endl;
        
        // Cruzar
        vector<Outfit> offspring = CrossOver(population, prendas_disponibles, diversity_control);

        // Mutar
        vector<Outfit> mutated_offspring = Mutate(offspring, t, armario_organizado, prendas_disponibles);
        
        // Evauar descendencia
        diversidad_generacion = Evaluate(mutated_offspring, weather_category, modelo, diversity_control );
        
        // Actualizar P(t)
        population = mutated_offspring;

        t++;
        LogGeneration(population, t, diversidad_generacion);
    }

    generateOutfitFolder(population, weather_category, modelo, diversity_control);
    return 0;
    
}

// Diversity = sum_i( sum_j( hammingDist(P[i], P[j]) ) ) / ( P.size() ** 2 * L)
// L: Length of chromosome 
// https://arxiv.org/ftp/arxiv/papers/1109/1109.0085.pdf

// Si la nueva solución corresponde a la clase, pero disminuye la diversidad de la población, entonces se ve penalizado
// https://www.cs.sjtu.edu.cn/~kzhu/papers/zhu-ecml04.pdf