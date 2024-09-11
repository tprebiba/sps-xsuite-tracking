/**
 * 
 */
package cern.accsoft.steering.jmad.modeldefs.defs.tt43tt41;

import cern.accsoft.steering.jmad.domain.file.CallableModelFileImpl;
import cern.accsoft.steering.jmad.domain.file.ModelFile;
import cern.accsoft.steering.jmad.domain.file.ModelPathOffsetsImpl;

import static cern.accsoft.steering.jmad.domain.types.enums.JMadPlane.H;

import cern.accsoft.steering.jmad.domain.file.CallableModelFile.ParseType;
import cern.accsoft.steering.jmad.domain.file.ModelFile.ModelFileLocation;
import cern.accsoft.steering.jmad.domain.machine.RangeDefinitionImpl;
import cern.accsoft.steering.jmad.domain.machine.SequenceDefinitionImpl;
import cern.accsoft.steering.jmad.domain.machine.filter.RegexNameFilter;
import cern.accsoft.steering.jmad.domain.result.tfs.TfsResult;
import cern.accsoft.steering.jmad.domain.twiss.TwissInitialConditionsImpl;
import cern.accsoft.steering.jmad.domain.types.enums.JMadPlane;
import cern.accsoft.steering.jmad.factory.BeamFactory;
import cern.accsoft.steering.jmad.modeldefs.ModelDefinitionFactory;
import cern.accsoft.steering.jmad.modeldefs.domain.JMadModelDefinition;
import cern.accsoft.steering.jmad.modeldefs.domain.JMadModelDefinitionImpl;
import cern.accsoft.steering.jmad.modeldefs.domain.OpticsDefinition;
import cern.accsoft.steering.jmad.modeldefs.domain.OpticsDefinitionImpl;

/**
 * This class is the actual model configuration for the TI2 transfer line.
 * 
 * @author Kajetan Fuchsberger (kajetan.fuchsberger at cern.ch)
 */
public class Tt43tt41ModelDefinitionFactory implements ModelDefinitionFactory {

    @Override
    public JMadModelDefinition create() {
        JMadModelDefinitionImpl modelDefinition = new JMadModelDefinitionImpl();
        modelDefinition.setName("TT43TT41");

        ModelPathOffsetsImpl offsets = new ModelPathOffsetsImpl();
        offsets.setResourceOffset("tt43tt41/2017");
        modelDefinition.setModelPathOffsets(offsets);

        modelDefinition.addInitFile(new CallableModelFileImpl("beam/tt43tt41.beam", ModelFileLocation.RESOURCE));
        modelDefinition.addInitFile(new CallableModelFileImpl("sequence/tt43tt41.seq", ModelFileLocation.RESOURCE));

        /*
         * OPTICS
         */
        String[] strengthFileNames = new String[] { "str/tt43tt41_initial_optics.str", "str/tt43tt41_new_mag_len.str",
                "str/tt43tt41_fint_06.str", "str/tt43tt41_fint_03.str", "str/tt43tt41_fint_01.str",
                "str/tt43tt41_edges.str", "str/tt43tt41_edges_fint.str", "str/tt43tt41_final.str" };

        for (String strengthFileName : strengthFileNames) {
            System.out.print("Optics create: ");
            System.out.println(strengthFileName);
            String opticsName = strengthFileName.replaceAll("str/", "2017_").replaceAll(".str", "");
            OpticsDefinition opticsDefinition = new OpticsDefinitionImpl(opticsName, new ModelFile[] {
                    new CallableModelFileImpl(strengthFileName, ModelFileLocation.RESOURCE, ParseType.STRENGTHS) });
            modelDefinition.addOpticsDefinition(opticsDefinition);
        }
        modelDefinition.setDefaultOpticsDefinition(modelDefinition.getOpticsDefinitions().get(0));

        /*
         * SEQUENCE
         */

        SequenceDefinitionImpl tt43 = new SequenceDefinitionImpl("tt43", null);
        modelDefinition.setDefaultSequenceDefinition(tt43);
        RangeDefinitionImpl tt43range = new RangeDefinitionImpl(tt43, "ALL", createT43InitialConditions());
        tt43.setDefaultRangeDefinition(tt43range);

        tt43range.addMonitorInvertFilter(new RegexNameFilter(".*", H));

        return modelDefinition;
    }

    /**
     * Twiss initial conditions for transferl+ine T66
     */
    private final TwissInitialConditionsImpl createT43InitialConditions() {
        TwissInitialConditionsImpl twissInitialConditions = new TwissInitialConditionsImpl("tt43-twiss");

        twissInitialConditions.setDeltap(0.0);
        twissInitialConditions.setBetx(5.0);
        twissInitialConditions.setAlfx(0.0);
        twissInitialConditions.setDx(0.0);
        twissInitialConditions.setDpx(0.0);
        twissInitialConditions.setBety(5.0);
        twissInitialConditions.setAlfy(0.0);
        twissInitialConditions.setDy(0.0);
        twissInitialConditions.setDpy(0.0);
        twissInitialConditions.setCalcAtCenter(true);
        twissInitialConditions.setClosedOrbit(false);
        return twissInitialConditions;

    }

}
